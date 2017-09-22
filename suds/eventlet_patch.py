import os

def apply():
    import eventlet
    eventlet.monkey_patch()

    import suds.version

    def yield_function(function):
        def wrapped(*args, **kwargs):
            eventlet.sleep(0)
            value = function(*args, **kwargs)
            eventlet.sleep(0)

            return value

        setattr(function.im_class, function.__name__, wrapped)

    import suds.sax.parser

    yield_function(suds.sax.parser.Handler.endElement)

    import suds.wsdl

    def _wdsl_definitions_open_import(self, imported_definitions):
        for imp in self.imports:
            eventlet.sleep(0)
            imp.load(self, imported_definitions)

    suds.wsdl.Definitions.open_imports = _wdsl_definitions_open_import

    yield_function(suds.wsdl.Definitions.add_children)
    yield_function(suds.wsdl.Definitions.set_wrapped)

    import suds.reader

    yield_function(suds.reader.DocumentReader.open)

    import suds.xsd.schema

    yield_function(suds.xsd.schema.Schema.build)
    yield_function(suds.xsd.schema.Schema.merge)
    yield_function(suds.xsd.schema.Schema.instance)

    import suds.umx.core

    yield_function(suds.umx.core.Core.append)

    import suds.xsd.sxbase

    yield_function(suds.xsd.sxbase.Iter.__init__)

if not os.environ.get('DISABLE_EVENTLET_PATCHING'):
    try:
        apply()
    except ImportError:
        pass
