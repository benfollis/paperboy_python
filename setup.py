from setuptools import setup
setup(name='paperboy_python',
      version="0.1",
      description="A python module that computes similarity from articles that were fetched from paperboy_fetcher",
      url="https://github.com/benfollis/paperboy_python",
      author="Ben Follis",
      license="GPLv3",
      packages=['paperboy'],
      install_requires=['tensorflow', 'tensorflow_hub', 'numpy'],
      zip_safe=False,
      scripts=['bin/paperboy'])