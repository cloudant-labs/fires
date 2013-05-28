from couchdbkit import Server, Database
from copy import deepcopy
import ConfigParser, sys, time, csv
from cpool import CloudantPool

def get_creds(f='/Users/mlmiller/.clou'):
    config = ConfigParser.ConfigParser()
    config.read(f)
    return {'user':config.get('cloudant','user'), 'pwd':config.get('cloudant','password')}
    
def formatDoc(doc):
    for k, v in doc.items():
        try:
            if k=='STATE':
                continue
            elif k=='ZIP'or k=='Fires' or k=='Major' or k=='Strucfires':
                doc[k] = int(v)
            else:
                doc[k] = float(v.replace('%',''))
        except: 
            doc[k] = None
    return doc

if __name__=='__main__':

    fname = sys.argv[1]
    print 'Import data from file:\t %s' % fname

    creds = get_creds()
    uri = 'https://%s:%s@%s.cloudant.com' % (creds['user'], creds['pwd'], creds['user'])
    print uri
    dbname = 'fires2013'
    
    #NUMBER OF DOCUMENTS TO UPLOAD
    nworkers = 20 #n_threads
    
    s = Server(uri)
    db = s.get_or_create_db(dbname)
    print db.info()
    
    #create writer pool
    pool = CloudantPool(nworkers, 100, 0.1, 1., uri, dbname)
    
    start = time.time()
    step = 1000
    ndocs =0
    docs = []

    for doc in csv.DictReader(open(fname, 'r'), delimiter='\t'):
        doc = formatDoc(doc)
        #print doc
        docs.append(doc)
        ndocs +=1 
        if len(docs)==step:
            pool.pushDoc(deepcopy(docs))
            del docs
            docs = []
    #don't forget final flush                
    pool.flush()
    
    delta = float(time.time()-start)
    rate = float(ndocs)/delta
    print 'Summary Statistics\n\nsaved:\t%i\tdocs in:\t%f\tseconds for:\t%f\tdocs/sec' % (ndocs, delta, rate)
    
