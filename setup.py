from distutils.core import setup

setup(
    name="Answerme Bot",
    version="1.0",
    packages = ['docs', 'modules', 'modules/message_processing','modules/my_multiset',],
    scripts = ['run.py'],
    author="Ivan Kosarevych",
    author_email="kosarevych@ucu.edu.ua",
)