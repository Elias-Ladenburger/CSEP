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

function copyToClipboard(clipboardText) {
    navigator.clipboard.writeText(clipboardText).then(function () {
        window.alert("Successfully copied to Clipboard");
        return true;
    }, function () {
        window.alert("Could not copy to clipboard automatically. " +
            "Please copy manually.");
        return true;
    });
}


function deleteElement(deleteURL, requestData, elemToRemove = "") {
    let confirmation = confirm('Do you really want to delete this element?')
    if (confirmation === true) {
        if (elemToRemove !== "") {
            $('#' + elemToRemove).remove();
        }
        jQuery.ajax({
            url: deleteURL,
            method: 'DELETE',
            data: requestData
        });
        window.reload();
    }
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
        /*
        btnScenarioTutorial: {
            text: 'Start Tutorial',
            icon: 'fas fa-graduation-cap',
            event: function () {
                window.location = $('#scenarios-table').data()['createUrl'];
            },
            attributes: {
                title: 'Start a tutorial to create a scenario'
            }
        },*/
    }
}

function removeImage(imageId = '#inject_image') {
    hideElement(imageId);
    $('remove_image').checked = true;
}

function resetForm(formId){
    let resetForm = document.getElementById(formId);
    let formElements = resetForm.elements;
    for(let i = 0; i<formElements.length;i++){
        let currentElement = formElements[i];
        if(currentElement.type === "text"){
            currentElement.value = "";
        }
        if(currentElement.tag === "select"){
            currentElement.value = "---";
        }
    }
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
    populateElement(detailsId, url);
    $('body').tooltip({selector: '[data-toggle=tooltip]'});
}

function elementIsHidden(elemId) {
    return $(elemId).offsetParent === null
}