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
        new_path = window.location.href
        console.log(new_path)
        if(window.location.pathname == '/meals/') {
            meal = $(this).find("td#col-name").children("span")[0].innerHTML
            new_path += meal
        } else if(window.location.pathname == '/admin/meals/') {
            meal = $(this).find("td#col-name").children("span")[0].innerHTML
            new_path += meal
        }
        window.location.href = new_path
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
            var selectCols = ["col-access", "col-Unit Options", "col-unit", "col-Foods"]
            if(selectCols.includes($(element).attr('id'))) {
                var selectOptions = JSON.parse($("#selectOptions").val());
                var disableCols = ["col-unit"]
                var disable = disableCols.includes($(element).attr('id')) && $(element).hasClass('disable')
                var newInput = $('<select></select>', {
                    'class': 'form-select created-input',
                    'style': disable ? 'background-color:grey;color:white;' : 'background-color:rgba(0,0,0,.3);color:white',
                });
                if(disable) { newInput.attr("disabled", "disabled") }
                var multiSelects = ["col-Unit Options", "col-Foods"]
                if(multiSelects.includes($(element).attr('id'))) { newInput.attr('multiple', 'multiple') }
                Object.entries(selectOptions).forEach(([key, value]) => {
                    var newOption = $('<option></option>', {
                        'text': key,
                        'value': value
                    });
                    if(multiSelects.includes($(element).attr('id'))) {
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
    var search = $("#table-search").val().toLowerCase()
    $(".item-row").each(function(i, row) {
        found = false
        $(row).children("td").children("span").each(function(j, col) {
            if(col.innerHTML.toLowerCase().includes(search)) {
                found = true
            }
        });
        if(!found) {
            $(row).addClass('d-none');
        } else {
            $(row).removeClass('d-none');
        }
    });
});

document.addEventListener("DOMContentLoaded", function() {
    var openMealModal = $("#openMealModal")
    if(openMealModal.val() == "true") {
        $("#createMealHiddenButton").click()
    }
});

$("#new_meal_foods").on("change", function(e) {
    var foods = $("#new_meal_foods")
    var foodVal = foods.val()
    var foodName = this.options[this.selectedIndex].innerHTML
    if(!isNaN(foodVal)) {
        var allFoods = JSON.parse($("#allFoods").val())
        var food = {}
        Object.entries(allFoods).forEach(([key, foodJSON]) => {
            if(foodJSON["id"] == foodVal) {
                food = foodJSON
            }
        })
        $("#new_meal_foods option[value='" + foodVal + "']").remove();
        var newFood = $('<div />', {
            'class': 'meal-food-item',
            'value': foodVal
        });
        newFood.append($('<div />', { 'class': 'food-col', 'col': 'name', 'html': foodName}))
        var amountInput = $('<input />', {
            'type': 'number',
            'style': 'background-color:rgba(0,0,0,.3);color:white',
            'class': 'food-col form-control created-input',
            'placeholder': 'Amount',
            'col': 'amount',
            'onchange': 'updateChosenFoods.call(this)'
        }).appendTo(newFood);
        var unitSelect = $('<select />', {
            'class': 'food-col form-select',
            'col': 'unit',
            'onchange': 'updateChosenFoods.call(this)'
        })
        var chooseUnit = $('<option selected>Choose Unit</option>').appendTo(unitSelect);
        Object.entries(food["units"]).forEach(([key, unit]) => {
            var unitOption = $('<option value="'+unit["id"]+'">'+unit["name"]+'</option>').appendTo(unitSelect)
        })
        newFood.append(unitSelect)
        newFood.append($('<div class="removeNewMealFood"><i onclick="removeNewMealFood.call(this)" class="fa-solid fa-circle-xmark" style="cursor:pointer;"></i></div>'))
        var mealFoods = $("#mealFoodContainer");
        mealFoods.append(newFood)
        var chosenFoods = JSON.parse($("#chosenFoods").val())
        chosenFoods.push({"id":foodVal, "name":foodName, "amount":0, "unit":null})
        $("#chosenFoods").val(JSON.stringify(chosenFoods))
    }
});

function removeNewMealFood() {
    var food = $(this).closest(".meal-food-item")
    var foodID = food.attr('value')
    var foodName = food.children("div[col='name']")[0].innerHTML
    var chosenFoods = JSON.parse($("#chosenFoods").val())
    chosenFoods = chosenFoods.filter( food => food.id !== foodID )
    $("#chosenFoods").val(JSON.stringify(chosenFoods))
    food.remove()
    var foods = $("#new_meal_foods")
    foods.append('<option value="' + foodID + '">' + foodName + '</option>')
}

function updateChosenFoods() {
    var col = $(this).attr('col')
    var val = $(this).val()
    var food = $(this).closest(".meal-food-item")
    var foodID = food.attr('value')
    var chosenFoods = JSON.parse($("#chosenFoods").val())
    chosenFoods = chosenFoods.map( food => {
        if(food.id == foodID) {
            food[col] = val
        } 
        return food
    })
    $("#chosenFoods").val(JSON.stringify(chosenFoods))
}

$("#meal-edit-button").on("click", function(e) {
    var button = $(this)
    var foodsContainer = button.parents("#meal-container").children("#foods-container")
    var inputs = foodsContainer.find("input, select")
    var icons = foodsContainer.find(".remove-icon")
    if(button.html() == "Edit") {
        button.html("Update")
        button.css('background-color', 'var(--bs-primary)')
        inputs.each(function(i, input) {
            $(input).attr("disabled", false)
        })
        icons.each(function(i, icon) {
            $(icon).removeClass('d-none')
        })
        $("#add-food-container").removeClass('d-none')
    } else {
        button.html("Edit")
        button.css('background-color', 'white')
        inputs.each(function(i, input) {
            $(input).attr("disabled", true)
        })
        icons.each(function(i, icon) {
            $(icon).addClass('d-none')
        })
        $("#add-food-container").addClass('d-none')

        var mealName = $("#mealName").val()
        var foods = JSON.parse($("#foodsJSON").val())
        var route = window.location.origin
        var path = window.location.pathname.includes("admin") ? "/admin/meals/update-meal" : '/meals/update-meal'
        route += path
        fetch(route, {
            method: "POST",
            headers: {'Content-Type': 'application/json'}, 
            body: JSON.stringify({"meal_name":mealName, "foods":foods})
        }).then(res => {
            console.log(res);
        });
    }
})

$(".remove-food").on("click", function(e) {
    removeFood.call(this)
})

$(".food-data").on("change", function(e) {
    foodDataUpdate.call(this)
})

$("#add-food-button").on("click", function(e) {
    var foodID = $("#new-food").val()
    var foodName = $("#new-food option:selected").text()
    if(foodName != 'Choose food') {
        var foodUnits = JSON.parse($("#new-food option:selected").attr("units"))
        $("#new-food option[value='" + foodID + "']").remove();
        var foods = JSON.parse($("#foodsJSON").val())
        foods.push({"id":Number(foodID), "name":foodName, "amount":0, "unit":null, "units": foodUnits})
        $("#foodsJSON").val(JSON.stringify(foods))
        var foodContainer = $(".food-container")[0]
        var newFoodContainer = foodContainer.cloneNode(true)
        $(newFoodContainer).find(".food-name").text(foodName)
        $(newFoodContainer).find(".remove-food").attr("id", foodID)
        $(newFoodContainer).find(".remove-food").on("click", function(e){ removeFood.call(this) })
        var foodAmount = $(newFoodContainer).find(".food-amount").find(".food-data")
        $(foodAmount).on("change", function(e){ foodDataUpdate.call(this) })
        $(foodAmount).attr("id", "amount-"+foodID)
        $(foodAmount).val(0)
        var foodUnit = $(newFoodContainer).find(".food-unit").find(".food-data")
        $(foodUnit).on("change", function(e){ foodDataUpdate.call(this) })
        $(foodUnit).empty().append("<option>Choose unit</option>")
        foodUnits.forEach(function(i, unit) {
            unit = foodUnits[unit]
            $(foodUnit).append("<option value='"+unit["id"]+"'>"+unit["name"]+"</option>")
        })
        $(foodUnit).attr("id", "unit-"+foodID)
        $(foodUnit).val([])
        $(foodUnit).prop("selectedIndex", 0)
        $(foodUnit).attr("units", JSON.stringify(foodUnits))
        $(newFoodContainer).insertAfter($("#add-food-container"))
    }
})

function foodDataUpdate() {
    var type = $(this).attr("name")
    var foodID = $(this).attr("id").split(type+"-")[1]
    var val = $(this).val()
    var foods = JSON.parse($("#foodsJSON").val())
    foods = foods.map( food => {
        if(food["id"] == foodID) {
            food[type] = Number(val)
        } 
        return food
    })
    $("#foodsJSON").val(JSON.stringify(foods))
}

function removeFood() {
    var foodID = $(this).attr("id")
    var foods = JSON.parse($("#foodsJSON").val())
    foods = foods.filter( food => food.id != foodID )
    $("#foodsJSON").val(JSON.stringify(foods))
    var foodContainer = $(this).parents(".food-container")
    var foodUnits = JSON.parse($(foodContainer).find(".food-unit").find(".food-data").attr("units"))
    var foodName = $(foodContainer).find(".food-name").text()
    $("#new-food").append("<option value='"+foodID+"' units='"+JSON.stringify(foodUnits)+"'>"+foodName+"</option>")
    foodContainer.remove()
}

$(".calendar-row-add").on("click", function(e) {
    var mealName = $(this).siblings("span")[0].innerHTML
    $("#selectedMealName").val(mealName)
    $(".modal-title")[0].innerHTML = "Update Calendar - " + mealName
})

$(".bought-button").on("click", function(e) {
    fetch("/shopping/update-bought", {
        method: "POST",
        headers: {'Content-Type': 'application/json'}, 
        body: JSON.stringify(
            {
                "id": $(this).closest(".item-row").find(".item-id").val(), 
                "bought": !$(this).hasClass("text-primary")
            }
        )
    }).then(res => {
        console.log(res);
        window.location.reload();
    });
})