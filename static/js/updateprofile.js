function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function (){
    $("#updatebutton").click(function (event){
       event.preventDefault();
       const firstName = $("#account-fn").val();
       const lastName = $("#account-ln").val();
       const email = $("#account-email").val();
       const username = $("#account-username").val();
       const countryoption = $("#account-country").find("option:selected");
       const country = countryoption.val();
       const cityoption = $("#account-city").find("option:selected");
       const city = cityoption.val();
       console.log(country);
       console.log(city);
       const address = $("#account-address").val();
       const zipcode = $("#account-zip").val();
       if(zipcode.length!==6){
            document.getElementById("account-display-msg").innerText = "Enter Valid Zip Code";
            document.getElementById("account-display-msg").style.color = "red";
       }
       else{
            const data = {
           'username' : username,
           'email': email,
           'firstName': firstName,
           'lastName': lastName,
           'country' : country,
           'city' : city,
           'address' : address,
           'zipcode' : zipcode,
           }
           console.log(window.location.href.split('/')[3])
            const authToken = window.location.href.split('/')[3]
           $.ajaxSetup(
                {
                    headers : {
                        "X-CSRFToken":getCookie('csrftoken'),
                    }
                }
            )
           $('#loaderprofile').removeClass('hidden')
            console.log(JSON.stringify(data))
            $.ajax({
                type: 'PUT',
                url: '/'+authToken+'/updateprofile',
                contentType: 'application/json',
                data: JSON.stringify(data), // access in body
            }).done(function (result) {
                $('#loaderprofile').addClass('hidden')
                if(result.status_msg === 'Ok'){
                    document.getElementById("account-display-msg").innerText = result.msg;
                    document.getElementById("account-display-msg").style.color = "green"
                    window.location.href='/'+authToken+'/account-profile';
                }
                else {
                    document.getElementById("account-display-msg").innerText = result.msg;
                    document.getElementById("account-display-msg").style.color = "red"
                }
            })
           }
    });
})