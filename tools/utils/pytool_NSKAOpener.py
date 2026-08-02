import sys
import plistlib
import pickle
import base64
import string
import datetime 

def userDisplayBytes(data: bytes) -> str:
    #return "GenericBytesData" #TODO change
    try:
        # 1. Attempt to decode to plaintext
        text = data.decode('utf-8')
        
        # 2. Check for hidden binary garbage (optional but recommended)
        # Allows common whitespace (\n, \t, \r) but rejects raw binary bytes
        printable = set(string.printable)
        if any(char not in printable for char in text):
            raise ValueError("Contains binary characters")
            
        return text  # Successfully returned as plaintext string
        
    except (UnicodeDecodeError, ValueError):
        # 3. Fallback: Encode to Base64 string
        b64_bytes = base64.b64encode(data)
        return b64_bytes.decode('utf-8')

def cleanObject(obj):
    if isinstance(obj, plistlib.UID): return obj.data
    elif isinstance(obj, (bytes, bytearray)): return userDisplayBytes(obj)
    elif isinstance(obj, list): return [cleanObject(subobject) for subobject in obj]
    elif isinstance(obj, dict): return {k: cleanObject(v) for k, v in obj.items()}
    elif isinstance(obj, (set, frozenset)): return list(obj)
    elif isinstance(obj, datetime.datetime):  # not a very good solution, if utc return in cocoa, otherwise dtSpread 
        utc = datetime.timezone.utc
        if obj.tzinfo == utc or obj.tzinfo is None:
            return (obj.replace(tzinfo=utc) - datetime.datetime(2001,1,1,tzinfo=utc)).total_seconds()
        return ["datetimeSpread", str(obj.tzinfo), (obj - datetime.datetime(2001,1,1,tzinfo=utc)).total_seconds()]
    else: return obj

def openNSObject(NSObjects,NSObjindex):
    end = len(NSObjects) - 1
    NSInfo = None
    NSObject = NSObjects[NSObjindex]

    if not isinstance(NSObject, dict):
        and_ = None
        if isinstance(NSObject, int) and len(NSObjects) >= NSObject: and_ = NSObjects[NSObject]
        return f"WHAT AM I: {NSObject} AND {and_}"


    if "$class" in NSObject:
        NSInfo = NSObjects[NSObject["$class"]]
    else:
        return "Empty class error"

    classname = NSInfo["$classname"]
    result = None

    if classname in ["NSMutableDictionary", "NSDictionary"]:
        result = {}

        for i, k_uid in enumerate(NSObject["NS.keys"]):
            kkey = k_uid.data
            vkey = NSObject["NS.objects"][i].data 
            key = NSObjects[kkey]
            value = NSObjects[vkey]

            if isinstance(value, dict) and "$class" in value:
                result[key] = openNSObject(NSObjects, vkey)
            else:
                result[key] = value
            
    elif classname in ["NSMutableSet", "NSSet", "NSMutableArray", "NSArray"]:
        result = []

        for obj in NSObject["NS.objects"]:
            key = obj.data
            value = NSObjects[key]
            if isinstance(value, dict) and "$class" in value:
                result.append(openNSObject(NSObjects, key))
            else:
                result.append(value)

    elif classname in ["NSMutableData", "NSData"]:
        result =  NSObject["NS.data"]
    elif classname == "NSDate":
        result =  NSObject["NS.time"]
    else:
        return f"Unknown NSType {classname}"

    return result


def openNSKeyedArchiverS(NSKAr):
    if NSKAr.get("$archiver") != "NSKeyedArchiver" or NSKAr.get("$version") != 100000:
        return cleanObject(NSKAr) #treating item as standard plist

    NSobjects = NSKAr.get("$objects")
    top = NSKAr.get("$top")

    if NSobjects[0] != "$null": print("there is a problem with the objects"); return None

    end = len(NSobjects) - 1

    if end == 1:
        return cleanObject(NSobjects[1])
    elif end < 1:
        return None
    else:
        return cleanObject(openNSObject(NSobjects, 1))

def open():
    if len(sys.argv) != 2:
        print("Incorrect Usage")
        sys.exit(1)

    dtype = sys.argv[1] #open as (stream, file)
    data = sys.stdin.buffer.read() 
    NSKAr = None

    if dtype == "file":
        NSKAr = plistlib.load(data)
    elif dtype == "stream":
        NSKAr = plistlib.loads(data)

    NSKAr = openNSKeyedArchiverS(NSKAr)
    sys.stdout.buffer.write(pickle.dumps(NSKAr))

    return

if __name__ == "__main__":
    open()