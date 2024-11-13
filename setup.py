from setuptools import setup
from Cython.Build import cythonize

"""
(lib) ➜  AutoTestX git:(dev) ✗ mkdir -p automation_web 
(lib) ➜  AutoTestX git:(dev) ✗ mkdir -p automation_app 
(lib) ➜  AutoTestX git:(dev) ✗ python setup.py build_ext --inplace 
切换分支删除缓存：
find . -name "*.pyc" -delete
find . -name "__pycache__" -exec rm -r {} +
"""


setup(
    name="AutoTestX",
    ext_modules=cythonize(
        [
            "task_executor/automation_executor.py",
        ],
        compiler_directives={'language_level': "3"}
    ),
    zip_safe=False,
)
