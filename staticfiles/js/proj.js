function closebutton()
{
    let alert =document.getElementById('button');
    alert.style.display = 'none';
}


let searchForm = document.getElementById('searchForm');
let pageLink = document.getElementsByClassName('page-link');

for(let i=0; i<pageLink.length;i++){
    pageLink[i].addEventListener('click',function (e){
        e.preventDefault();
        
        let page = this.dataset.page;
        searchForm.innerHTML += `<input name="page" value=${page} hidden/>`;
        console.log('clicked');
        searchForm.submit();
    })

}