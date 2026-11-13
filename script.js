document.getElementById("year").textContent=new Date().getFullYear();
const menu=document.querySelector(".menu-button");
const navs=document.querySelectorAll(".nav");
menu.addEventListener("click",()=>{const open=menu.getAttribute("aria-expanded")!=="true";menu.setAttribute("aria-expanded",String(open));navs.forEach(n=>n.classList.toggle("open",open));});
navs.forEach(n=>n.querySelectorAll("a").forEach(a=>a.addEventListener("click",()=>{navs.forEach(x=>x.classList.remove("open"));menu.setAttribute("aria-expanded","false");})));
document.querySelectorAll(".filter").forEach(button=>button.addEventListener("click",()=>{document.querySelectorAll(".filter").forEach(b=>b.classList.remove("is-active"));button.classList.add("is-active");const type=button.dataset.filter;document.querySelectorAll(".journal-card").forEach(card=>{card.hidden=type!=="all"&&card.dataset.kind!==type;});}));
