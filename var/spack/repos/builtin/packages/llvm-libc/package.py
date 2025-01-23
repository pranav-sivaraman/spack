# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class LlvmLibc(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://libc.llvm.org/"
    url = "https://github.com/llvm/llvm-project/archive/refs/tags/llvmorg-19.1.7.tar.gz"
    git = "https://github.com/llvm/llvm-project"

    maintainers("pranav-sivaraman")

    license("Apache-2.0", checked_by="pranav-sivaraman")

    version("main", branch="main")
    version("19.1.7", sha256="59abea1c22e64933fad4de1671a61cdb934098793c7a31b333ff58dc41bff36c")

    depends_on("cxx", type="build")
    depends_on("cmake@3:20:", type="build")

    depends_on("python@3.8:", type="build")
    depends_on("py-pyyaml@5.1:", type="build")

    conflicts("gcc@:12.1")
    conflicts("clang@:10")

    root_cmakelists_dir = "runtimes"

    def cmake_args(self):
        args = [
            self.define("LLVM_ENABLE_RUNTIMES", "libc;compiler-rt"),
            self.define("LLVM_LIBC_FULL_BUILD", True),
            self.define("LLVM_LIBC_INCLUDE_SCUDO", True),
            self.define("COMPILER_RT_BUILD_SCUDO_STANDALONE_WITH_LLVM_LIBC", True),
            self.define("COMPILER_RT_BUILD_GWP_ASAN", False),
            self.define("COMPILER_RT_SCUDO_STANDALONE_BUILD_SHARED", False),
        ]

        return args
