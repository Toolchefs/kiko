
from kiko.operators.curveoperator import curveoperator
from kiko.operators.bakeoperator import bakeoperator
from kiko.operators.staticoperator import staticoperator
from kiko.operators.worldspaceoperator import worldspaceoperator
from kiko.operators.factory import OperatorsFactory

_initialized = False

def initialize():
    global _initialized

    if not _initialized:
        _initialized = True

        factory = OperatorsFactory()
        factory.register(staticoperator.StaticOperator)
        factory.register(curveoperator.CurveOperator)
        factory.register(bakeoperator.BakeOperator)
        factory.register(worldspaceoperator.WorldSpaceOperator)
