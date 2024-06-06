$(".row-select").on("click", function(e) {
    var table = $(this).closest(".table");
    if(this.checked) {
        activateTool("editButton");
        activateTool("deleteButton");
        $(this).parents(".item-row").addClass("table-active");
        if($(".row-select").not(":checked").length == 0) {
            $(table).find(".selectAllItems").prop("checked", true);
        }
    } else {
        if($(".row-select:checked").length == 0) {
            deactivateTool("editButton");
            deactivateTool("deleteButton");
            deactivateTool("updateButton");
        }
        $(this).parents(".item-row").removeClass("table-active");
        $(table).find(".selectAllItems").prop("checked", false);
    }
    e.stopPropagation();
});

$(".selectAllItems").on("click", function() {
    var table = $(this).closest(".table");
    if(this.checked) {
        activateTool("editButton");
        activateTool("deleteButton");
        $(table).find(".item-row").addClass("table-active");
        $(table).find(".row-select").prop("checked", true);
    } else {
        deactivateTool("editButton");
        deactivateTool("deleteButton");
        deactivateTool("updateButton");
        makeUneditable();
        $(table).find(".item-row").removeClass("table-active");
        $(table).find(".row-select").prop("checked", false);
    }
});

$(".item-row").on("click", function(e) {
    if(!$(".editButton").hasClass("active-link") && $(".table-clickable").length) {
        console.log("GO TO USER ACCOUNT PAGE")
    }
});

function selectedRows() {
    return $(".form-check-input:checked");
}

function stopProp(e) {
    e.stopPropagation();
}

$(".editButton").on("click", function() {
    if(!$(this).hasClass("disabled-tool")) {
        $(this).toggleClass("active-link");
        if($(this).hasClass("active-link")) {
            deactivateTool("deleteButton");
            activateTool("updateButton");
            makeEditable();
        } else {
            deactivateTool("updateButton");
            activateTool("deleteButton");
            makeUneditable();
        }
    }
});

$(".deleteButton").on("click", function() {
    if(!$(this).hasClass("disabled-tool")) {
        var deleteItems = [];
        $(".row-select:checked").each(function(i, element) {
            deleteItems.push($(element).closest(".item-row").find(".item-id").val());
        });
        $("#delete-items").val(JSON.stringify(deleteItems));
    }
});

$(".updateButton").on("click", function() {
    if(!$(this).hasClass("disabled-tool")) {
        var updateItems = [];
        $(".row-select:checked").each(function(i, row) {
            var updateItem = {};
            var closestRow = $(row).closest(".item-row");
            updateItem['id'] = closestRow.find(".item-id").val();
            closestRow.find("td").each(function(i, element) {
                var col = $(element).attr('id').split("-")[1];
                updateItem[col] = $(element).find(".created-input").val();
            });
            updateItems.push(updateItem);
        });
        $("#update-items").val(JSON.stringify(updateItems));
    }
});

function activateTool(tool) {
    var toolElement = $("."+tool);
    toolElement.removeClass("disabled-tool");
    if(toolElement.hasClass("createModal")) {
        var toolType = toolElement.attr('id').split("-")[1];
        toolElement.attr("data-bs-toggle", "modal").attr("data-bs-target", "#" + toolType + "ItemsModal");
    }
}

function deactivateTool(tool) {
    var toolElement = $("."+tool);
    toolElement.addClass("disabled-tool");
    if(toolElement.hasClass("createModal")) {
        var toolType = toolElement.attr('id').split("-")[1];
        toolElement.removeAttr("data-bs-toggle", "modal").removeAttr("data-bs-target", "#" + toolType + "ItemsModal");
    }
    toolElement.removeClass("active-link");
}

function makeEditable() {
    $(".row-select:checked").each(function(i, check) {
        $(check).closest(".item-row").find("td").each(function(i, element) {
            var newInput = null;
            var span = $(element).find("span");
            $(span).addClass("d-none");
            var currentVal = span.text();
            var selectCols = ["col-access", "col-Unit Options", "col-unit"]
            if(selectCols.includes($(element).attr('id'))) {
                var selectOptions = JSON.parse($("#selectOptions").val());
                var newInput = $('<select></select>', {
                    'class': 'form-select created-input'
                });
                if($(element).attr('id') == "col-Unit Options") { newInput.attr('multiple', 'multiple') }
                Object.entries(selectOptions).forEach(([key, value]) => {
                    var newOption = $('<option></option>', {
                        'text': key,
                        'value': value
                    });
                    if($(element).attr('id') == "col-Unit Options") {
                        var vals = currentVal.split(", ")
                        vals.forEach((val) => {
                            if(val == key) { newOption.attr("selected", true) }
                        })
                    } else {
                        if(currentVal == key) { newOption.attr("selected", true) }
                    }
                    newInput.append(newOption);
                });
            } else {
                var dateCols = ["col-expiration"]
                var disableCols = ["col-name"]
                var disable = disableCols.includes($(element).attr('id')) && $(element).hasClass('disable')
                var newInput = $('<input />', {
                    'type': dateCols.includes($(element).attr('id')) ? 'date' : 'text',
                    'style': disable ? 'background-color:grey;color:white;' : 'background-color:rgba(0,0,0,.3);color:white',
                    'class': 'form-control created-input',
                    'value': currentVal
                });
                if(disable) { newInput.attr("disabled", "disabled") }
            }
            $(element).append(newInput);
        });
    });
    $(".row-select").attr("disabled", true);
    $(".selectAllItems").attr("disabled", true);
}

function makeUneditable() {
    $(".created-input").each(function(i, element) {
        $(element).siblings().removeClass('d-none');
        $(element).remove();
    });
    $(".row-select").attr("disabled", false);
    $(".selectAllItems").attr("disabled", false);
}

$("#table-search").on("input", function(e) {
    var search = $("#table-search").val()
    $(".item-row").each(function(i, row) {
        found = false
        $(row).children("td").children("span").each(function(j, col) {
            if(col.innerHTML.includes(search)) {
                found = true
            }
        });
        if(!found) {
            $(row).addClass('d-none');
        } else {
            $(row).removeClass('d-none');
        }
    });
    // var table = $(this).closest(".table");
    // if(this.checked) {
    //     activateTool("editButton");
    //     activateTool("deleteButton");
    //     $(this).parents(".item-row").addClass("table-active");
    //     if($(".row-select").not(":checked").length == 0) {
    //         $(table).find(".selectAllItems").prop("checked", true);
    //     }
    // } else {
    //     if($(".row-select:checked").length == 0) {
    //         deactivateTool("editButton");
    //         deactivateTool("deleteButton");
    //         deactivateTool("updateButton");
    //     }
    //     $(this).parents(".item-row").removeClass("table-active");
    //     $(table).find(".selectAllItems").prop("checked", false);
    // }
    // e.stopPropagation();
});