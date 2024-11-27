from setuptools import setup
from Cython.Build import cythonize

"""
(lib) ➜  AutoTestX git:(dev) ✗ mkdir -p automation_web 
(lib) ➜  AutoTestX git:(dev) ✗ mkdir -p automation_app 
(lib) ➜  AutoTestX git:(dev) ✗ python setup.py build_ext --inplace 
切换分支删除缓存：find . -name "*.pyc" -delete
"""


setup(
    name="AutoTestX",
    ext_modules=cythonize(
        [
            "task_executor/automation_executor.py",
            "task_executor/automation_api/api_parameter_handler.py",
            "task_executor/automation_app/action_perform_operation.py",
            "task_executor/automation_web/web.py",
            "initialize.py",
        ],
        compiler_directives={'language_level': "3"}
    ),
    zip_safe=False,
)
