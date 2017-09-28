import urllib2
from urllib2 import urlopen
from xml.dom import minidom
import argparse
import sys

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('repoUrl', help='repository url')
parser.add_argument('package', help='package name')
parser.add_argument('artifact', help='artifact name')
parser.add_argument('version', help='version like 2.2 or 2.9-SNAPSHOT')
parser.add_argument('extension', help='artifact\'s extension')
parser.add_argument('--classifier', help='optional artifact classifier')
parser.add_argument('--path', help='local path prefix where to save')



args = parser.parse_args()
if args.classifier == None:
    args.classifier = ''

if args.repoUrl == None or args.package == None or args.artifact == None or args.version == None or args.version == None or args.extension == None:
    parser.print_help()
    sys.exit(0)

args.package = args.package.replace('.','/')

if args.path == None:
    args.path = ''
elif (not args.path.endswith('\\')) and (not args.path.endswith('/')):
    args.path = args.path + '/'

def getUrl(itemValue, itemClassifier, itemExtension):
    if len(itemClassifier) > 0:
        itemClassifier = '-' + itemClassifier
    return [args.repoUrl + '/' + args.package + '/' + args.artifact + '/' + args.version + '/' , args.artifact + '-' + itemValue + itemClassifier+'.' + itemExtension]

fileUrl = []

try:
    if (args.version.endswith('SNAPSHOT')):
        response = urllib2.urlopen(args.repoUrl+'/'+args.package+'/'+args.artifact + '/'+args.version+ '/maven-metadata.xml')
        html = response.read()
        xmldoc = minidom.parseString(html)
        for v in xmldoc.getElementsByTagName('snapshotVersion'):
            classifierList = v.getElementsByTagName('classifier')
            itemExtension = v.getElementsByTagName('extension')[0].firstChild.nodeValue
            itemValue = v.getElementsByTagName('value')[0].firstChild.nodeValue
            if len(args.classifier)>0 and len(classifierList) > 0:
                itemClassifier = classifierList[0].firstChild.nodeValue
                if args.classifier == itemClassifier:
                    fileUrl = getUrl(itemValue, itemClassifier, itemExtension)
                    break
            else:
                if itemExtension == args.extension:
                    fileUrl = getUrl(itemValue, '', itemExtension)
                    break
    else:
        fileUrl = getUrl(args.version, args.classifier, args.extension)

    response = urlopen(''.join(fileUrl))
    file = args.path + fileUrl[1]
    print ''.join(fileUrl),'-->',file
    CHUNK = 16 * 1024
    with open(file, 'wb') as f:
        while True:
            chunk = response.read(CHUNK)
            if not chunk:
                break
            f.write(chunk)
except urllib2.HTTPError as e:
    print e.msg
except IOError as e:
    print e.strerror, ':', args.path

