from lib.urlObject import UrlObject
testing = [ 'https://securit.ie/users/testing/hax.html?test=1',
            'https://securit.ie/users/testing/hax?test=1',
            'https://securit.ie/users/testing/nothing/',
            'https://securit.ie/users/hax?test=1',
            'https://securit.ie/users',
            'https://securit.ie/users.test.html',
            'https://securit.ie/']

for i in testing:
    u = UrlObject(i)
    print('url: '+i)
    print('u_d: '+u.u_d)
    print('u_dd: '+u.u_dd)
    print('u_q: '+u.u_q)
    print('full: '+u.full)
    print('fullpath: '+u.fullpath)
    print('host: '+u.host)
    print('query: '+u.query)
    print('lastpath: '+u.lastpath)
    print('lastfile: '+u.lastfile)
    print('lastfile_ext: '+u.lastfile_ext)
    print('last_ext: '+u.last_ext)
    print('------------------\n')
