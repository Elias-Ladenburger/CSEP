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

function showFormModal(modalId='', targetUrl = '') {
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
