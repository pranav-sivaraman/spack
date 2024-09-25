# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.variant import _a_single_value_or_a_combination


class LlvmRedux(CMakePackage):
    """The LLVM Project is a collection of modular and reusable
    compiler and toolchain technologies."""

    homepage = "https://llvm.org/"
    url = "https://github.com/llvm/llvm-project/archive/llvmorg-7.1.0.tar.gz"
    git = "https://github.com/llvm/llvm-project"

    license("Apache-2.0", checked_by="pranav-sivaraman")

    version("19.1.0", sha256="0a08341036ca99a106786f50f9c5cb3fbe458b3b74cab6089fd368d0edb2edfe")

    # TODO: Add conditionals for ALL variants as we go back LLVM versions
    # TODO: Add conflicts between projects and runtimes (they must not intersect)
    # TODO: add compiler conflicts and dependency conflicts

    # TODO: Project Conflicts
    # flang needs clang,mlir

    variant(
        "projects",
        default="clang",
        description="",
        values=(
            "bolt",
            "clang",
            "clang-tools-extra",
            "compiler-rt",
            "cross-project-tests",
            "flang",
            "libc",
            "libclc",
            "lld",
            "lldb",
            "mlir",
            "openmp",
            "polly",
            "pstl",
        ),
        multi=True,
    )

    variant(
        "runtimes",
        default=("libunwind", "libcxxabi", "libcxx"),
        description="",
        values=(
            "libc",
            "libunwind",
            "libcxxabi",
            "pstl",
            "libcxx",
            "compiler-rt",
            "openmp",
            "llvm-libgcc",
            "offload",
        ),
        multi=True,
    )

    variant(
        "targets",
        description="",
        values=(
            _a_single_value_or_a_combination(
                "all",
                *(
                    "AArch64",
                    "AMDGPU",
                    "ARM",
                    "AVR",
                    "BPF",
                    "Hexagon",
                    "Lanai",
                    "LoongArch",
                    "Mips",
                    "MSP430",
                    "NVPTX",
                    "PowerPC",
                    "RISCV",
                    "Sparc",
                    "SystemZ",
                    "VE",
                    "WebAssembly",
                    "X86",
                    "XCore",
                ),
            )
        ),
    )

    variant(
        "experimental-targets",
        description="",
        values=any_combination_of("ARC", "CSKY", "DirectX", "M68k", "SPIRV", "Xtensa"),
    )

    # TODO: Add conflicts with LLVM
    variant(
        "bolt-targets",
        description="",
        values=_a_single_value_or_a_combination("all", *("AArch64", "X86", "RISCV")),
        when="projects=bolt",
    )

    variant(
        "libclc-targets",
        description="",
        values=_a_single_value_or_a_combination(
            "all",
            *(
                "amdgcn--",
                "amdgcn--amdhsa",
                "clspv--",
                "clspv64--",
                "r600--",
                "nvptx--",
                "nvptx64--",
                "nvptx--nvidiacl",
                "nvptx64--nvidiacl",
            ),
        ),
        when="projects=libclc",
    )

    # LLVM
    variant(
        "ffi",
        default=False,
        description="Use libffi to call external functions from the interpreter",
    )
    variant("libxml2", default=True, description="Use libxml2")
    variant("libedit", default=True, description="Use libedit")
    variant("libpfm", default=True, description="Use libpfm for performance counters")
    variant("zlib", default=True, description="Use zlib for compression/decompression")
    variant("zstd", default=True, description="Use zstd for compression/decompression")
    variant("curl", default=False, description="Use libcurl for the HTTP client")
    variant("httplib", default=False, description="Use cpp-httplib HTTP server library")
    variant("z3", default=False, description="Enable Support for the Z3 constraint solver")

    # clang

    # TODO: Need OR syntax
    # pstl
    for condition in ("projects=pstl", "runtimes=pstl"):
        variant(
            "pstl-backend",
            default="serial",
            description="",
            values=("serial", "tbb", "omp"),
            multi=False,
            when=condition,
        )

    # TODO: add cxxstd
    # TODO: add compiler conflicts with cxxstd (tho this can happen in mainline spack)
    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("cmake@3.20:", type="build")

    # LLVM
    depends_on("python@3.8:", type=("build", "run"))
    depends_on("libffi", when="+ffi")
    depends_on("libxml2", when="+libxml2")
    depends_on("libedit", when="+libedit")
    depends_on("libpfm4", when="+libpfm")
    depends_on("zlib-api", when="+zlib")
    depends_on("zstd", when="+zstd")
    depends_on("curl", when="+curl")
    depends_on("cpp-httplib", when="+httplib")
    depends_on("z3@4.8.9:", when="+z3")

    with when("projects=clang"):
        depends_on("perl", type="test")
        depends_on("libxml2@2.5.3:")

    # pstl
    depends_on("tbb", when="pstl-backend=tbb")
    # TODO: add pstl libomp, right now its implicit

    # TODO: Add the option for standalone builds?
    # Default is "runtimes" build using clang
    # Alternative is "standalone". So can a package reuse itself or should be standalone?
    root_cmakelists_dir = "llvm"

    def cmake_args(self):
        spec = self.spec
        define = self.define
        from_variant = self.define_from_variant

        projects = ";".join(spec.variants["projects"].value)
        runtimes = ";".join(spec.variants["runtimes"].value)
        
        if spec.variants["targets"].value == "all":
            targets = "all"
        else:
            targets = ";".join(spec.variants["targets"].value)
        
        # TODO: simplify to checking the list
        if spec.variants["experimental-targets"].value == "all":
            experimental_targets = "all"
        elif spec.variants["experimental-targets"].value == "none":
            experimental_targets = ""
        else:
            experimental_targets = ";".join(spec.variants["experimental-targets"].value)
            
        # LLVM
        args = [
            define("LLVM_ENABLE_PROJECTS", projects),
            define("LLVM_ENABLE_RUNTIMES", runtimes),
            define("LLVM_TARGETS_TO_BUILD", targets),
            define("LLVM_EXPERIMENTAL_TARGETS_TO_BUILD", experimental_targets),
            from_variant("LLVM_ENABLE_FFI", "ffi"),
            from_variant("LLVM_ENABLE_LIBXML2", "libxml2"),
            from_variant("LLVM_ENABLE_LIBEDIT", "libedit"),
            from_variant("LLVM_ENABLE_LIBPFM", "libpfm"),
            from_variant("LLVM_ENABLE_ZLIB", "zlib"),
            from_variant("LLVM_ENABLE_ZSTD", "zstd"),
            from_variant("LLVM_ENABLE_CURL", "curl"),
            from_variant("LLVM_ENABLE_HTTPLIB", "httplib"),
            from_variant("LLVM_ENABLE_Z3_SOLVER", "z3"),
            define("LLVM_INCLUDE_TESTS", self.run_tests),
        ]

        if spec.variants["bolt-targets"].value == "all":
            bolt_targets = "all"
        else:
            bolt_targets = ";".join(spec.variants["bolt-targets"].value)

        # bolt
        args.extend(
            [
                define("BOLT_TARGETS_TO_BUILD", bolt_targets),
                define("BOLT_INCLUDE_TESTS", self.run_tests),
            ]
        )

        # clang
        args.extend(
            [
                from_variant("CLANG_ENABLE_LIBXML2", "libxml2"),
                define("CLANG_INCLUDE_TESTS", self.run_tests),
            ]
        )

        # flang

        # pstl
        args.append(from_variant("PSTL_PARALLEL_BACKEND", "pstl-backend"))

        return args
