import sys,os,hashlib
import json
import shutil
  

def send_file(file,settings):
    print >> sys.stderr, "DEBUG Sending file with settings %s" % settings
    
    directory = settings.get('directory')
    filename = settings.get('filename')
    
    activation_key = settings.get('activationkey')
    app_name = "Scheduled Export of Indexed Data (SEND) to File"
    
    m = hashlib.md5()
    m.update((app_name))
    if not m.hexdigest().upper() == activation_key.upper():
        print >> sys.stderr, ("FATAL Activation key for App '%s' failed" % app_name)
        sys.exit(2)
    
    try:  
        
        dstfile =  os.path.join(directory, filename)
        shutil.copy(file, dstfile) 
    
        return True  
    except Exception as tre:  
        print >> sys.stderr,tre  
        return False  
    except:  
        e = sys.exc_info()[0]  
        print >> sys.stderr, "ERROR Error sending file: %s" % e  
        return False  
  
  
if __name__ == "__main__":  
    if len(sys.argv) > 1 and sys.argv[1] == "--execute":  
        payload = json.loads(sys.stdin.read())
        if not send_file(payload.get('results_file'),payload.get('configuration')):
            print >> sys.stderr, "FATAL Failed trying to send file"
            sys.exit(2)
        else:
            print >> sys.stderr, "INFO file successfully sent"
    else:
        print >> sys.stderr, "FATAL Unsupported execution mode (expected --execute flag)"
        sys.exit(1)
