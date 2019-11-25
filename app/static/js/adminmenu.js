//from app import wrapper
// call wrapper.functionName
//-----------------------------------------------------------------------

class dayMeal{
    // dayMeal has 5 properties: dayMeal, desc, day, meal, and weekend (boolean)
    constructor(dayMeal, descr){
        console.log("creating new dayMeal object");
        this.dayMeal = dayMeal;
        this.descr = descr;
        var days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
        var meals = ["Breakfast", "Lunch", "Dinner"];
        var validDayMeal=0
        for (var i = 0; i < days.length; i++) {
            if (dayMeal.includes(days[i])) {
                validDayMeal=1
                this.day = i;
                if (days[i] == "Sunday" || days[i] == "Monday") {
                    this.weekend = true;
                }
                else {
                    this.weekend = false;
                }
                for (var j = 0; j < meals.length; j++) {
                    if (dayMeal.includes(meals[j])) {
                        this.meal = j;
                    }
                }
            }
            
        }
        if (!validDayMeal) {
            console.log("id has an invalid dayMeal: " + dayMeal);
        }
    }
}
 
//-----------------------------------------------------------------------

function addInputField(dayMeal){
    if (document.getElementById('adding' + dayMeal) == null) {
        var modify = document.getElementsByClassName(dayMeal.toString());
        var currList = modify[0].parentNode;
        var add = document.createElement("li");
        add.classList.add("list-group-item");
        add.classList.add("inputTextFieldLI");
        add.innerHTML = "<input type='text' class='inputTextField' id='adding" + dayMeal + "' onkeypress='addItem(event, this)'>";
        var addbefore = document.getElementById('addButton'+dayMeal).parentNode;
        currList.insertBefore(add, addbefore);
    }
    return;
}


//-----------------------------------------------------------------------

// need to write this function to allow admin to enter an item's description
function editDescription(e, element){
   
}
//-----------------------------------------------------------------------


//-----------------------------------------------------------------------
function removeItem(element, mealDescr){
    element.parentNode.remove();
    $.post('/adminmenu', {item: mealDescr, dayMeal: "", day: "", add: "remove"});
    console.log("Removing from db item: " + mealDescr);
}
//-----------------------------------------------------------------------

function addItem(e, element){

    // immediately exit if key pressed was not enter
    if (e.keyCode != 13) return;

    // access which day and meal this input is for
    var accessID = element.id.toString();
    accessID = accessID.replace("adding", "");
    mealDescr = element.value;
    itemInfo = new dayMeal(accessID, mealDescr);
    console.log("Access ID: ", accessID);
    console.log("this item is for day #: ", itemInfo.day);
    console.log("this item is for meal #: ", itemInfo.meal);
    console.log("this item's description is: ", itemInfo.descr);

    // return if no input
    if ((mealDescr.length) < 1) {
        console.log("No input");
        return;
    }

    console.log('the inputted item is', element.value);

    $.post('/adminmenu', {item: itemInfo.descr, dayMeal: itemInfo.meal, day: itemInfo.day, add: "add"});

    // add this input to the front-end menu
    var modify = document.getElementsByClassName(itemInfo.dayMeal.toString());
    console.log(dayMeal.toString());
    console.log('modify is ', modify[0]);
    var currList = modify[0].parentNode;
    var add = document.createElement("li");
    add.classList.add("list-group-item");
    add.classList.add("menu-item");
    add.innerHTML = mealDescr;
    var buttonString = '<button onclick=removeItem(this,"' + mealDescr.toString() + '") id="removeButton' + itemInfo.dayMeal + '"">&times;</button>';
    add.innerHTML += (buttonString);
    var addbefore = document.getElementById('addButton'+itemInfo.dayMeal).parentNode;
    currList.insertBefore(add, addbefore);

    // Remove the addInput element
    element.parentNode.remove();
    
    return;

}
//-----------------------------------------------------------------------

// on page load
document.addEventListener("DOMContentLoaded", function(event) { 
    var topNavHeight = $('#top-navbar').outerHeight() ;
    $('#first-element').css('margin-top', topNavHeight);

    console.log('js is working');
   
});
