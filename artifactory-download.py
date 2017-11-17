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

def getText(nodelist):
    # Iterate all Nodes aggregate TEXT_NODE
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
        else:
            # Recursive
            rc.append(getText(node.childNodes))
    return ''.join(rc)

fileUrl = []

try:
    if (args.version.endswith('SNAPSHOT')):
        response = urllib2.urlopen(args.repoUrl+'/'+args.package+'/'+args.artifact + '/'+args.version+ '/maven-metadata.xml')
        html = response.read()
        xmldoc = minidom.parseString(html)
        for v in xmldoc.getElementsByTagName('snapshotVersion'):
            classifierList = v.getElementsByTagName('classifier')
            itemClassifier = getText(classifierList)
            itemExtension = v.getElementsByTagName('extension')[0].firstChild.nodeValue
            itemValue = v.getElementsByTagName('value')[0].firstChild.nodeValue
            if args.classifier == itemClassifier and itemExtension == args.extension:
                fileUrl = getUrl(itemValue, itemClassifier, itemExtension)
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
