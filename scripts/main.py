import hou
import os
import json
import random
import toolutils as tu

home = hou.homeHoudiniDirectory()

jpath = f'{home}\\packages\\hou_interpreter\\demo.json'
tpath = f'{home}\\packages\\hou_interpreter\\text.json'

def loadJson(path: str):
    if os.path.exists(path) and path.endswith('.json'):
        fd = os.open(path, os.O_RDONLY)
        fsize = os.path.getsize(path)
        fdata = os.read(fd, fsize)
        os.close(fd)
        return json.loads(fdata.decode())
    else:
        raise FileNotFoundError(path)

nodes = {}
jdatas = loadJson(jpath)
tdatas = loadJson(tpath)

spare_input_text = tdatas['spare_input']

#init selection nodes
selected_nodes = hou.selectedNodes()

for jdata in jdatas:
    nodeId = jdata.get('id')
    if nodeId >= 0:
        #init parent node
        context = jdata.get('parentNodeContext', 'obj')
        context_nodeId = jdata.get('parentNodeId', 0)
        par_node = None
        if context == 'node':
            par_node = nodes.get(context_nodeId)
        elif context == 'dopnet':
            par_node = hou.currentDopNet()
        elif context == 'parent':
            try:
                par_node = nodes.get(context_nodeId).parent()
            except:
                par_node = nodes.get(context_nodeId)
        else:
            par_node = hou.node(context)

        #create node
        node_type = jdata.get('type')
        node = par_node.createNode(node_type)

        #rename node
        if jdata.get('name', '') != '':
            node.setName(jdata.get('name'))

        #set node parms
        for jparm in jdata.get('parms', []):
            parm = node.parm(jparm.get('name'))
            parmValue = jparm.get('value')

            #format strings
            pathTypes = ['absolute', 'relative']
            parmValueType = jparm.get('valueType', 'none')
            formatedParmValue = parmValue
            if parmValueType in pathTypes:
                parmNodeId = jparm.get('nodeId')
                parmPath = ''
                if parmValueType == 'absolute':
                    parmPath = nodes[parmNodeId].path()
                elif parmValueType == 'relative':
                    parmPath = nodes[parmNodeId].relativePathTo(node)
                formatedParmValue = formatedParmValue.format(parmPath)
            elif parmValueType == 'seed':
                formatedParmValue.format(random.randint(0, 1000))

            #set parm value
            try:
                parm.set(formatedParmValue)
            except:
                parm.setExpression(formatedParmValue)
            finally:
                if jparm.get('oneTimeExperession', False):
                    parm.deleteAllKeyframes()

        #set node inputs
        for jinput in jdata.get('inputs', []):
            inputId = jinput.get('inputId', 0)
            inputNode = nodes.get(jinput.get('nodeId'))
            if inputId >= 0:
                outputId = jinput.get('outputId', 0)
                node.setInput(inputId, inputNode, outputId)
            else:
                #spare input

                #init texts
                nSpareInput = -inputId - 1
                spareInputTags = spare_input_text['tags']
                spareInputName = spare_input_text['name'].format(nSpareInput)
                spareInputLabel = spare_input_text['label'].format(nSpareInput)
                spareInputHelp = spare_input_text['help'].format(inputId)

                #init parm
                spareInputTemplate = hou.StringParmTemplate(spareInputName, spareInputLabel, 1)
                spareInputTemplate.setStringType(hou.stringParmType.NodeReference)
                spareInputTemplate.setDefaultValue(('', ))
                spareInputTemplate.setTags(spareInputTags)
                spareInputTemplate.setHelp(spareInputHelp)

                #set parm
                node.addSpareParmTuple(spareInputTemplate)
                relativePath = node.relativePathTo(inputNode)
                node.parm(spareInputName).set(relativePath)

        #node operations
        ops = jdata.get('operations', {})
        selected = ops.get('selected', False)
        forceSelected = ops.get('forceSelected', False)
        displayed = ops.get('displayed', False)
        rendered = ops.get('rendered', False)
        framed = ops.get('framed', False)
        node.setSelected(selected, forceSelected)
        node.setGenericFlag(hou.nodeFlag.Display, displayed)
        node.setGenericFlag(hou.nodeFlag.Render, rendered)
        if framed:
            ne = tu.networkEditor()
            ne.setCurrentNode(node)
        node.moveToGoodPosition()
    else:
        if len(selected_nodes) >= -nodeId:
            node = selected_nodes[-nodeId - 1]
        else:
            ne = tu.networkEditor()
            node = ne.currentNode()
        
        #filter node
        node_type = jdata.get('type', '')
        if node.type().name() != node_type and node_type != '':
            raise hou.NodeError()
    
    #add to dict
    nodes[nodeId] = node