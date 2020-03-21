from common.basedir import BASEDIR
is_in_travis = BASEDIR.strip('/').split('/')[0] != 'data'
