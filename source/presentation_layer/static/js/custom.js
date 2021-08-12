$(document).ready(function () {
    $('[data-role="tags-input"]').tagsInput();
    $('[data-toggle="tooltip"]').tooltip();
    $('[data-toggle="popover"]').popover();
    const url = window.location.href;
    loadTab(url);
});

function detailFormatter(index, row, element) {
    let html = []
    const wanted_details = ["description", "scenario_description", "title", "target_group", "learning_objectives", "required_knowledge"]
    $.each(row, function (key, value) {
        if (wanted_details.includes(key)) {
            key = key.replace("scenario", "")
            key = key.replace("_", " ")
            html.push('<p><b>' + key + ':</b> ' + value + '</p>')
        }
    })
    return html.join('')
}

function deleteScenario(scenario_id) {
    const deleteURL = $('#scenarios-table').data()["deleteUrl"];
    $('#' + scenario_id).remove();
    jQuery.ajax({
        url: deleteURL,
        method: 'DELETE',
        data: {
            scenario_id: scenario_id
        }
    });
    window.reload();
}

function loadTab(url) {
    if (url.indexOf("#") > 0) {
        let activeTab = url.substring(url.indexOf("#") + 1);
        $('.nav[role="tablist"] a[href="#' + activeTab + '"]').tab('show');
    }

    $('ul[role="tab"]').on("click", function () {
        let newUrl;
        const hash = $(this).attr("href");
        newUrl = url.split("#")[0] + hash;
        history.replaceState(null, null, newUrl);
    });
}

function renderNetwork(networkId, injectData, edgeData) {
    // create a network
    for (let i = 0; i < injectData.length; i++) {
        let tmp_node = injectData[i];
        if (tmp_node.hasOwnProperty("is_entry_node") && injectData[i]["is_entry_node"] === true) {
            tmp_node["label"] += ":entry point";
           tmp_node["color"] = 'orange';
        }
        else if(tmp_node["label"] === "condition"){
            tmp_node["color"] = "lightgreen";
            tmp_node["size"] = 4;
            tmp_node["label"] = "";
            tmp_node["hidden"] = true;
        }
    }
    let injects = new vis.DataSet(injectData);
    let injectConnections = new vis.DataSet(edgeData);
    let container = document.getElementById(networkId);

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
        edges: {
            arrows: {to: {enabled: true, type: "arrow"}},
            smooth: {type: "curvedCW"}
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

function scenario_table_buttons() {
    return {
        btnAddScenario: {
            text: 'Create scenario',
            icon: 'fas fa-plus-square',
            event: function () {
                const createUrl = $('#scenarios-table').data()['createUrl'];
                showFormModal('#scenario-form-modal');
            },
            attributes: {
                title: 'Add a new scenario',
                class: 'btn btn-primary'
            }
        },
        btnScenarioTutorial: {
            text: 'Start Tutorial',
            icon: 'fas fa-graduation-cap',
            event: function () {
                window.location = $('#scenarios-table').data()['createUrl'];
            },
            attributes: {
                title: 'Start a tutorial to create a scenario'
            }
        },
    }
}

function removeImage(imageId = '#inject_image') {
    hideElement(imageId);
    $('remove_image').checked = true;
}

function variableTableButtons() {
    return {
        btnAdd: {
            text: 'New Variable',
            icon: 'fas fa-plus-square',
            event: function () {
                const createUrl = $('#variablesTable').data()["createUrl"];
                showFormModal('#variable-form-modal', createUrl);
            },
            attributes: {
                title: 'Add a new variable to this scenario'
            }
        },
    }
}

function showFormModal(modalId = '', targetUrl = '') {
    let modal = $(modalId);
    if (targetUrl !== '') {
        $.get(targetUrl, function (data) {
            modal.find('.modal-content').html(data);
        });
        modal.modal('show');
    } else {
        modal.modal('show');
    }
}

function populateElement(elemId = '', sourceUrl = '') {
    let elem = $(elemId);
    if (sourceUrl !== '') {
        $.get(sourceUrl, function (data) {
            elem.find('.remote-content').html(data);
        });
        $(elemId).show();
    } else {
        $(elemId).show();
    }
}

function hideElement(elemId = '') {
    let elem = $(elemId);
    elem.find('.remote-content').html('')
    elem.hide();
}

function showElement(elemId = '') {
    $(elemId).show();
}

function getMapHeight() {
    return (window.innerHeight - 120);
}

function deleteVariable(variableName, rowId) {
    let confirmation = confirm('Do you really want to delete the variable ' + variableName + '?')
    document.getElementById(rowId).remove();
    if (confirmation === true) {
        const deleteURL = $('#variablesTable').data()["deleteUrl"];
        jQuery.ajax({
            url: deleteURL,
            method: 'DELETE',
            data: {
                variable_name: variableName
            }
        });
    }
}

function renderInjectDetails(url, showForm = false) {
    const detailsId = '#inject-details';
    const formId = '#inject-form';
    if (showForm) {
        populateElement(formId, url)
    } else if (elementIsHidden(detailsId)) {
        hideElement(formId);
        populateElement(detailsId, url);
    } else {
        hideElement(detailsId);
        populateElement(formId, url);
    }
    $('body').tooltip({selector: '[data-toggle=tooltip]'});
}

function elementIsHidden(elemId) {
    return $(elemId).offsetParent === null
}