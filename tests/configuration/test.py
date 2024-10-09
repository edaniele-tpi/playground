import copy, json, os, shutil, unittest
from importlib_resources import files
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from airfoilsimulator.config.variables import INPUTDICT
from airfoilsimulator.core.modules.base import warn
from airfoilsimulator.core.modules.i_o import read_input
##############################################################################80
#
class Test(unittest.TestCase):
  '''
    Test
    
    A simple class to test the airfoilsimulator.config.variables module.
  '''
  location = os.path.dirname(os.path.abspath(__file__))
  #   
#
  def test_schema(self):
    '''
      Test the schema validation for the input file.

      Sources
      -------
      https://python-jsonschema.readthedocs.io/en/stable/
    '''
    print('\n')
    cwd = os.getcwd()
    os.chdir(self.location)
    #
    # copy airfoil geometry coordinates
    shutil.copy(
      os.path.join(files('airfoilsimulator.data'), 'DU96W180.dat'),
      os.path.join(os.getcwd(), 'airfoil.dat'),
    )
    #
    schemas_path = files('playground.schemas')
    exclude = 'airfoilsimulator'
    endswith = '.schema.json'
    subschemas = []
    for f in os.listdir(schemas_path):
      if os.path.isfile(os.path.join(schemas_path, f))\
        and f.endswith(endswith) and not exclude in f:
        subschemas.append(os.path.join(schemas_path, f))
    print('\nsub schemas:\t', subschemas)
    #
    # registry
    from referencing import Registry, Resource
    #
    __subschemas__ = []
    for file in subschemas:
      with open(file) as f:
        __subschemas__.append(json.load(f))
      print('\nsub schemas:\t', type(__subschemas__[-1]), __subschemas__[-1])
    with open(os.path.join(files('playground.schemas'), exclude+endswith)) as f:
      mainschema = json.load(f)
    print('\nmain schema:\t', type(mainschema), mainschema)
    #
    resources = []
    for ss in __subschemas__:
      resources.append(Resource.from_contents(ss,))
    registry = Registry().with_resources(
      [
        (__subschemas__[i]['$id'], resources[i]) for i in range(len(resources))
      ],
    )
    #
    # schema
    from jsonschema import Draft202012Validator
    validator = Draft202012Validator(
      schema=mainschema,
      registry=registry,  # the critical argument, our registry from above
    )
    #
    # input test
    with open(INPUTDICT) as f:
      input_test = json.load(f)
    print('\nTest input:\n'+str(input_test))
    #
    # validate
    try:
      validator.validate(instance=input_test)
    except ValidationError as e:
      warn(
        '\nValidation result error:\n\t'
        +str(e.json_path)
        +'\n\t'+str(e.validator_value)
        +'\n\t'+str(e.validator)
        +'\n\t'+str(e.message)
      )
      raise AssertionError()
    #
    d = read_input(input=INPUTDICT, validated=True)
    #
    os.chdir(cwd)
    #
    return
#
  def test_registry(self):
    '''
      Test registry use in validation.
      See https://python-jsonschema.readthedocs.io/en/stable/referencing/#in-memory-schemas
    '''
    print('\n')
    cwd = os.getcwd()
    os.chdir(self.location)
    #
    from referencing import Registry, Resource
    #
    with open(os.path.join(files('playground.schemas'), 'address.json')) as f:
      address = json.load(f)
    print(type(address), address)
    with open(os.path.join(files('playground.schemas'), 'customer.json')) as f:
      customer = json.load(f)
    print(type(customer), customer)
    #
    resources = Resource.from_contents(address,)
    registry = Registry().with_resources(
      [
        (address['$id'], resources),
        # (customer['id'], customer),
      ],
    )
    #
    from jsonschema import Draft202012Validator
    #
    with open(INPUTDICT) as f:
      input = json.load(f)
    #
    validator = Draft202012Validator(
      schema=customer,
      registry=registry,  # the critical argument, our registry from above
    )
    validator.validate(input)
    print('\nassertion valid:', validator.is_valid(input))
    #
    basename = os.path.basename(INPUTDICT)
    if not ':' in basename:
      basename = os.getcwd()
    validated_input = os.path.join(
      basename, INPUTDICT.split('.')[0]+'_validated.'+INPUTDICT.split('.')[-1]
    )
    print(customer['properties'])
    # input_list = [
    #   (prop : input[prop]) for prop in list(customer['properties'])
    # ]
    # output_dict = {}
    # for key, value in input_list:
    #     output_dict[key] = value
    # with open(validated_input, 'w+') as f:
    #   json.dump(
    #     dict(
    #       [(]
    #     ), f, indent=2
    #   )
    # assert not validator.is_valid({"foo": -37})  # Uh oh!
    #
    os.chdir(cwd)
    #
    return
#
if __name__ == '__main__':
    unittest.main()
##############################################################################80
# End.