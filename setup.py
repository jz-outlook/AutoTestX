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
            "task_executor/automation_web/SMS_verification.py",
            "task_executor/automation_web/web.py",
            "task_executor/automation_app/check_elements.py",
            "task_executor/automation_app/assert_operation.py"
        ],
        compiler_directives={'language_level': "3"}
    ),
    zip_safe=False,
)
