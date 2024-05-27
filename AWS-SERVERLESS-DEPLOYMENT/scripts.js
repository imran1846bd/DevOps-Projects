// Add your API endpoint here
var API_ENDPOINT = "https://9gjw459w92.execute-api.us-east-1.amazonaws.com/prod";

// Function to save student data
document.getElementById("savestudent").onclick = function() {
    var inputData = {
        "studentid": $('#studentid').val(),
        "name": $('#name').val(),
        "class": $('#class').val(),
        "age": $('#age').val()
    };
    $.ajax({
        url: API_ENDPOINT,
        type: 'POST',
        data: JSON.stringify(inputData),
        contentType: 'application/json; charset=utf-8',
        success: function(response) {
            document.getElementById("studentSaved").innerHTML = "Student Data Saved!";
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.error("Error saving student data: ", textStatus, errorThrown);
            alert("Error saving student data.");
        }
    });
}

// Function to retrieve all students
document.getElementById("getstudents").onclick = function() {  
    $.ajax({
        url: API_ENDPOINT,
        type: 'GET',
        contentType: 'application/json; charset=utf-8',
        success: function(response) {
            $('#studentTable tr').slice(1).remove();
            jQuery.each(response, function(i, data) {          
                $("#studentTable").append("<tr> \
                    <td>" + data['studentid'] + "</td> \
                    <td>" + data['name'] + "</td> \
                    <td>" + data['class'] + "</td> \
                    <td>" + data['age'] + "</td> \
                </tr>");
            });
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.error("Error retrieving student data: ", textStatus, errorThrown);
            alert("Error retrieving student data.");
        }
    });
}
