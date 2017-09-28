python artifactory-download.py -h
usage: artifactory-download.py [-h] [--classifier CLASSIFIER] [--path PATH]
                               repoUrl package artifact version extension

Process some integers.

positional arguments:
  repoUrl               repository url
  package               package name
  artifact              artifact name
  version               version like 2.2 or 2.9-SNAPSHOT
  extension             artifact's extension

optional arguments:
  -h, --help            show this help message and exit
  --classifier CLASSIFIER
                        optional artifact classifier
  --path PATH           local path prefix where to save



examples:
    python artifactory-download.py http://yourartifactoryhost:8080/artifactory/libs-snapshot-local my.package.path loader 2.9-SNAPSHOT jar --classifier jar-with-dependencies
    python artifactory-download.py http://yourartifactoryhost:8080/artifactory/libs-release-local my.second.path org-apache-commons-commons-vfs2 2.1 jar
    python artifactory-download.py http://yourartifactoryhost:8080/artifactory/libs-release-local my.second.path org-apache-commons-commons-vfs2 2.1 jar --path /home/john/jars
