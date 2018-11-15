function editOrder(){
    alert("You have clicked a parcel delivery order for editing!");

}
function deleteOrder(){
    alert("You have deleted a parcel delivery order!");

}
/*function to verify user or admin*/
function Verify(){
    var username = document.querySelector("#username").value;
    var password = document.querySelector("#password").value;
    if(username==='user' && password ==="user"){
       window.location.href ="vieworder.html";
    }else if(username==='admin' && password ==="admin"){
      var username = document.querySelector("#username").value;
      var password = document.querySelector("#password").value;
      window.location.href ="admin.html";
  
    }else{
    }
  }
  