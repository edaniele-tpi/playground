import unittest, importlib, importlib.metadata, os
#
class installed_package(object):
  def __init__(self, key, version):
    '''
      Constructor.
    '''
    #
    self.key = key
    self.version = version
    #
    return
#
def get_installed_distributions(verbose: bool = False):
  '''
    Returns installed distribution as `installed_package` object.
  '''
  ds = [d for d in importlib.metadata.distributions()]
  ip = []
  for d in ds:
    try:
      d._path
    except:
      pass
    else:
      if verbose: print(str(d._path)+'\t:\tversion:\t'+d.version)
      name = None
      if '.egg' in os.path.basename(str(d._path))\
        or '.dist' in os.path.basename(str(d._path)):
        name = os.path.basename(str(d._path))
      else:
        name = os.path.basename(os.path.dirname(str(d._path)))
      if verbose: print('distro:\t'+name)
      name_ = None
      for i, n in enumerate(name):
        if n == '-':
          name_ = name[:i]
          break
      if '.' in name_:
        name_ = name_.split('.')[0]
      if verbose: print('name:\t'+name_)
      ip.append(
        installed_package(key=name_, version=d.version)
      )
  #
  return ip
#
class Test(unittest.TestCase):
  '''
    Test class
  '''
  def test_a(self):
    '''
      Test a.
    '''
    installed_packages = get_installed_distributions()
    # installed_packages = pkg_resources.working_set
    installed_packages_list = sorted(
      ["%s==%s" % (i.key, i.version) for i in installed_packages]
    )
    print('\nInstalled packages list:')
    for p in installed_packages_list:
      print('\t'+p)
    print('\nImport all packages:')
    for i in installed_packages:
      try:
        importlib.import_module(i.key)
      except Exception as e:
        # try with character replacement
        try:
          importlib.import_module(i.key.replace('-','_'))
        except Exception as e:
          if 'scikit' in i.key:
            new_key = 'sk'+i.key.split('-')[-1]
            try:
              importlib.import_module(new_key)
            except Exception as e:
              print('\tException found:\t'+str(e))
            else:
              print('\tSuccessfully imported:\t'+new_key)
        else:
          print('\tSuccessfully imported:\t'+i.key.replace('-','_'))
      else:
        print('\tSuccessfully imported:\t'+i.key)
    #
    return
#
if __name__ == '__main__':
  unittest.main()
##############################################################################80
# End.
