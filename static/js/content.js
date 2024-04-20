var animationElements = document.querySelectorAll('.show-on-scroll')


function AddClassStart(element){
    // Bắt khi mình scroll
    var rectEl = element.getClientRects()[0];
    console.log(rectEl)
    // Câu lệnh lấy ra chiều cao màn hình 
    const heightWin = window.innerHeight
    // Kiểm tra khối xem có bên trong màn hình hay không
    if (!(rectEl.bottom <0 || rectEl.top >heightWin)){
        element.classList.add('start')
    }else{
        element.classList.remove('start')
    }
}

function CheckAnimation(){
    animationElements.forEach(el=>{
        AddClassStart(el)
    })
}

window.onscroll = CheckAnimation
console.log()
// window.addEventListener("scroll", function() {
//     // Hiển thị thông báo khi người dùng cuộn trang
//     alert("Bạn đang cuộn trang!");
// });