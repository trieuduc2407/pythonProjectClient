const AllVeh = document.getElementById('all-vehicles');
const Sedans = document.getElementById('Sedans-Couples');
const Suvs = document.getElementById('Crossovers-SUVs');
const Cert = document.getElementById('Certified');
const Future = document.getElementById('Future');
const searchBar = document.getElementById('searchInput');

//console.log(searchBar);
const leftNavItems = [AllVeh, Sedans, Suvs, Cert, Future];
AllVeh.classList.add('active');
let indexItems = [1, 0, 0, 0, 0]; // Index of the active nav item in each category

let render_vehicles = document.querySelector("#presentation-cars .img-render");
//console.log(render_vehicles);
function imgItem(linkUrl, className, classText, text){
    return `<div class = ${className}>
                <img src=${linkUrl} alt="car-image">
                <p class = ${classText}>${text}</p>
            </div>`
}


const requestOptions = {
    method: "GET",
    redirect: "follow"
  };
let data;
async function getData() {
    const reponse = await fetch("https://project-infinity-car-f8a94-default-rtdb.firebaseio.com/Product.json", requestOptions) 
    const result = await reponse.json(); 
    console.log(result)
    for(let i = 1; i <= Object.keys(result).length; i++) {
        let item = result[`pd${i}`];
        render_vehicles.insertAdjacentHTML('beforeend', imgItem(`${item['img']}`, 'img-item', 'text-img',  `${item['name']}`));
    }
    return result;
}
    // Function to update the display with new vehicle
    getData();

    function searchCar(name_in){
        getData().then((res)=>{
            let tmp_size = render_vehicles.childNodes.length;
            while(tmp_size > 0) {
                render_vehicles.removeChild(render_vehicles.lastChild);
                tmp_size = render_vehicles.childNodes.length;
            }
            data = res
            for(let i = 1; i <= Object.keys(data).length; i++) {
                let item = data[`pd${i}`];
                console.log(typeof(item['name']));
                if (item["name"].toLowerCase().includes(name_in.toLowerCase())) {
                    render_vehicles.insertAdjacentHTML('beforeend', imgItem(`${item['img']}`, 'img-item', 'text-img',  `${item['name']}`));
                }
             }
        })
    }
    searchBar.addEventListener("keyup",(e) =>{
        let filter = e.target.value.toLowerCase();
        searchCar(filter)
    })


    const showAll = () => {
        getData().then((res)=>{
            let tmp_size = render_vehicles.childNodes.length;
            while(tmp_size > 0) {
                render_vehicles.removeChild(render_vehicles.lastChild);
                tmp_size = render_vehicles.childNodes.length;
            }
            data = res
            console.log(data);
            for(let i = 1; i <= Object.keys(data).length; i++) {
                let item = data[`pd${i}`];
                //console.log(item)
                render_vehicles.insertAdjacentHTML('beforeend', imgItem(`${item['img']}`, 'img-item', 'text-img',  `${item['name']}`));
             }
        })
        
    }
    const showSedans = () => {
        getData().then((res)=>{
            let tmp_size = render_vehicles.childNodes.length;
            console.log(tmp_size);
            while(tmp_size > 0) {
                render_vehicles.removeChild(render_vehicles.lastChild);
                tmp_size = render_vehicles.childNodes.length;
            }
            console.log(tmp_size);
            data = res
            for(let i = 1; i <= Object.keys(data).length; i++) {
                let item = data[`pd${i}`];
                if (item["type"] !== "Sedan"){continue;}
                console.log(item)
                render_vehicles.insertAdjacentHTML('beforeend', imgItem(`${item['img']}`, 'img-item', 'text-img',  `${item['name']}`));
             }
             tmp_size = render_vehicles.childNodes.length;
             console.log(tmp_size);
        })
    }


    const showSuvs = () => {
        
        getData().then((res)=>{
            let tmp_size = render_vehicles.childNodes.length;
            while(tmp_size > 0) {
                render_vehicles.removeChild(render_vehicles.lastChild);
                tmp_size = render_vehicles.childNodes.length;
            }
            data = res
            for(let i = 1; i <= Object.keys(data).length; i++) {
                let item = data[`pd${i}`];
                if (item["type"] === "Suv"){
                    console.log(item)
                    render_vehicles.insertAdjacentHTML('beforeend', imgItem(`${item['img']}`, 'img-item', 'text-img',  `${item['name']}`));
                }
                
             }
        })
    }

    let subHeader = document.getElementsByClassName('sub-header')[0];

    const setActive = (item) => {
        idx = 0;
        for(let i = 0; i < indexItems.length; i++){
            if(item === leftNavItems[i]){
                idx = i;
                break;
            }
        }
        for(let j = 0; j < indexItems.length; j++) {
            if(j !== idx) {
                indexItems[j] = 0;
                leftNavItems[j].classList.remove('active');
            }
        }
        leftNavItems[idx].classList.add('active');
        indexItems[idx] = 1;
    }

    for(let i = 0; i < leftNavItems.length; i++) {
        leftNavItems[i].addEventListener("click", (e) => {
            e.preventDefault();
            setActive(leftNavItems[i]);
            switch (i){
                case 0 : 
                    showAll();
                    break;
                case 1: 
                    showSedans();
                    break;
                case 2: 
                    showSuvs();
                    break;
            }
           
        })
    }


    const showSubnav = () => {
        subHeader.classList.remove('no-display');
    }
    const hideSubnav = () => {
        subHeader.classList.add('no-display');
    }
    let vehicleBtn = document.getElementById("vehicle-btn");
    let closeSubnav = document.querySelector('.sub-nav button');
    vehicleBtn.addEventListener('click', (e)=>{
        e.preventDefault();
        if(subHeader.classList.contains('no-display')){
            showSubnav();
        } else{
            hideSubnav();
        }
        
    })
    closeSubnav.addEventListener('click', (e) => {
        e.preventDefault();
        hideSubnav();
    } )

   
    




