import unittest
#
class Test(unittest.TestCase):
  '''
    Test class
  '''
  def test_a(self):
    '''
      Test a.
    '''
    import pkg_resources
    import importlib
    installed_packages = pkg_resources.working_set
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
        print('\tException found:\t'+str(e))
      else:
        print('\tSuccessfully imported:\t'+i.key)
    #
    return
#
if __name__ == '__main__':
  unittest.main()
##############################################################################80
# End.