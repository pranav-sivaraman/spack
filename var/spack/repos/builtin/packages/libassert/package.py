# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *

class Libassert(CMakePackage):
    """The most over-engineered C++ assertion library"""

    homepage = "https://github.com/jeremy-rifkin/libassert"
    url = "https://github.com/jeremy-rifkin/libassert/archive/refs/tags/v2.1.0.tar.gz"
    
    maintainers("pranav-sivaraman")

    license("MIT", checked_by="pranav-sivaraman")

    version("2.1.0", sha256="e42405b49cde017c44c78aacac35c6e03564532838709031e73d10ab71f5363d")

    variant("shared", default=False, description="Build shared libs")
    variant("sanitizers", default=False, description="Build with sanitizers")
    variant("magic-enum", default=False, description="Use magic_enum library to print better diagnostics for enum classes")
    # variant("tests", default=False, description="Enable tests")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("cmake@3.14:", type="build")

    depends_on("cpptrace@0.6.0:")
    depends_on("magic-enum@0.9.5:", when="+magic-enum")

    def cmake_args(self):
        define = self.define
        from_variant = self.define_from_variant
        
        args = [
            from_variant("BUILD_SHARED_LIBS", "shared"),
            # from_variant("LIBASSERT_BUILD_TESTING", "tests"),
            from_variant("LIBASSERT_SANITIZER_BUILD", "sanitizers"),
            from_variant("LIBASSERT_USE_MAGIC_ENUM", "magic-enum"),
            define("LIBASSERT_USE_EXTERNAL_MAGIC_ENUM", "ON"),
            define("LIBASSERT_USE_EXTERNAL_CPPTRACE", "ON"),
        ]
        
        return args
