function renderNetwork(networkId, injectData, edgeData) {
    let nodeData = renderNodes(injectData);
    let connectionData = renderEdges(edgeData);

    // create a network
    let injects = new vis.DataSet(nodeData);
    let injectConnections = new vis.DataSet(connectionData);
    let container = document.getElementById(networkId);
    debugger;
    let data = {
        nodes: injects,
        edges: injectConnections,
    };
    let options = {
        autoResize: false,
        width: "80%",
        height: getMapHeight() + "px",
        clickToUse: false,
        interaction: {
            navigationButtons: true,
            dragNodes: false,
            dragView: true,
        },
        layout: {hierarchical: true},
        physics: {
            hierarchicalRepulsion: {
                nodeDistance: 120,
                avoidOverlap: 0.6
            }

        },
    };
    $(window).on('resize', function () {
        network.setOptions({
            height: getMapHeight() + "px",
        });
    });

    let network = new vis.Network(container, data, options);
    network.stabilize();
    return network;
}

function renderNodes(injectData) {
    for (let i = 0; i < injectData.length; i++) {
        let tmp_node = injectData[i];
        if (tmp_node.hasOwnProperty("is_entry_node") && injectData[i]["is_entry_node"] === true) {
            tmp_node["label"] += ":entry point";
            tmp_node["color"] = 'orange';
        } else if (tmp_node["label"] === "condition") {
            tmp_node["color"] = "lightgreen";
            tmp_node["size"] = 4;
            tmp_node["label"] = "";
            tmp_node["hidden"] = true;
        }
    }
    return injectData;
}

function renderEdges(edgeData) {
    for (let i = 0; i < edgeData.length; i++) {
        let edge = edgeData[i];
        let roundness = 0.4;
        let type = "curvedCW";
        edge["arrows"] = {to: {enabled: true, type: "arrow"}};
        if (!edge.hasOwnProperty("smooth")) {
            edge["smooth"] = {enabled: true, type: type, roundness: roundness};
            for (let j = i + 1; j < edgeData.length; j++) {
                let newEdge = edgeData[j];
                if (edge["from"] === newEdge["from"] && edge["to"] === newEdge["to"]) {
                    roundness = roundness + 0.3;
                    type = (type === "curvedCW") ? "curvedCCW" : "curvedCW";
                    newEdge["smooth"] = {enabled:true, type: type, roundness: roundness};
                }
            }
        }
    }
    return edgeData;
}