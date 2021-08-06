$(document).ready(function () {
    $('[data-role="tags-input"]').tagsInput();
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

function scenario_table_buttons() {
    return {
        btnAddScenario: {
            text: 'Create scenario',
            icon: 'fas fa-plus-square',
            event: function () {
                window.location = $('#scenarios-table').data()['createUrl'];
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


Array.prototype.move = function (start_index, target_index) {
    this.splice(start_index, 0, this.splice(target_index, 1)[0]);
};

Array.prototype.moveUp = function (start_index) {
    this.move(start_index, start_index - 1)
};

Array.prototype.moveDown = function (start_index) {
    this.move(start_index, start_index + 1)
};

function buildObjectArrayFromHTML(objectID = '.ol', selectorElement = 'li') {
    return $(objectID).find(selectorElement).map(function () {
        var item = {};
        item.title = $(this).attr("title");
        return item;
    });
}

function buildStoryListFromObject(storyList) {
    let stories = [];
    for (let i = 0; i < storyList.length; i++) {
        stories.push(storyList[i].title);
        //add injects
    }
    return stories;
}


function addTableRow(tableId = "editable-table", numberOfCells = 4, framename = null) {
    let table = document.getElementById(tableId);
    if (table == null) {
        table = document.getElementById(framename).contentWindow.document.getElementById(tableId);
    }
    let row = table.insertRow();
    for (let i = 0; i++; i < numberOfCells) {
        row.insertCell();
    }
}

function variableTableButtons() {
    return {
        btnAdd: {
            text: 'New Variable',
            icon: 'fas fa-plus-square',
            event: function () {
                $('#variable-modal-title').html('Add a variable');
                $('#variable-form-modal').modal('show');
            },
            attributes: {
                title: 'Add a new variable to this scenario'
            }
        },
    }
}

function deleteVariable(variableName, rowId) {
    let confirmation = confirm('Do you really want to delete the variable ' + variableName + '?')
    if (confirmation === true) {
        const deleteURL = $('#variablesTable').data()["deleteUrl"];
        jQuery.ajax({
            url: deleteURL,
            method: 'DELETE',
            async: false,
            data: {
                variable_name: variableName
            },
            success: function (data) {
                let remote = data;
            }
        });
        return remote;
        //.contentDocument.location.reload(true)
    }
}