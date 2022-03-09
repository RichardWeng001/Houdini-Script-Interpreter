import hou
import os
import json
import toolutils as tu

home = hou.homeHoudiniDirectory()

jpath = f'{home}\\packages\\hou_interpreter\\demo.json'

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

#init selection nodes
counter = -1
for node in hou.selectedNodes():
    nodes[counter] = node
    counter -= 1

for jdata in jdatas:
    if jdata['id'] >= 0:
        #init parent node
        context = jdata['parentNodeContext']
        par_node = None
        if context == 'node':
            par_node = nodes[jdata['parentNodeId']]
        elif context == 'dopnet':
            par_node = hou.currentDopNet()
        elif context == 'parent':
            par_node = nodes[jdata['parentNodeId']].parent()
        else:
            par_node = hou.node(context)

        #create node
        node = par_node.createNode(jdata['type'])

        #rename node
        if jdata['name'] != '':
            node.setName(jdata['name'])

        #set node parms
        for jparm in jdata['parms']:
            parm = node.parm(jparm['name'])
            try:
                parm.set(jparm['value'])
            except:
                parm.setExpression(jparm['value'])
            if jparm['oneTimeExperession']:
                parm.deleteAllKeyframes()

        #set node inputs
        for jinput in jdata['inputs']:
            inputId = jinput['inputId']
            inputNode = nodes[jinput['nodeId']]
            outputId = jinput['outputId']
            node.setInput(inputId, inputNode, outputId)

        #node operations
        ops = jdata['operations']
        node.setSelected(ops['selected'], ops['forceSelected'])
        node.setGenericFlag(hou.nodeFlag.Display, ops['displayed'])
        node.setGenericFlag(hou.nodeFlag.Render, ops['rendered'])
        if ops['framed']:
            ne = tu.networkEditor()
            ne.setCurrentNode(node)
        node.moveToGoodPosition()

        #add to dict
        nodes[jdata['id']] = node