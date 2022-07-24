const txt1 = document.getElementById('tbuser');
const btn1 = document.getElementById('btn1');
stock = "";

function fun1() {
    stock = txt1.value;
}
btn1.addEventListener('click', fun1);



  //js

//   $(document).ready(function () {
  
//     $("nav-link").click(function (){
//       $(this).addClass("active").siblings().removeClass("active");
//     });
//   });
  