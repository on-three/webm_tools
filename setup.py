# vim: set ts=2 expandtab:
from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='webm_tools',
  version='0.1',
  description='Tools to make webms. For me.',
  long_description = readme(),
	classifiers=[
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2.7',
    'Topic :: Multimedia :: Video :: Conversion',
  ],
  keywords = 'nsv mp4 webm conversion',
  url='https://github.com/on-three/webm_tools',
  author='on_three',
  author_email='on.three.email@gmail.com',
  license='MIT',
  packages=[
    'webm_tools',
  ],
  entry_points = {
    'console_scripts': [
      'mp42webm=webm_tools.mp42webm:main',
			'nsv2mp4=webm_tools.nsv2mp4:main',
      'gif2webm=webm_tools.gif2webm:main',
    ],
  },
  zip_safe=True)
