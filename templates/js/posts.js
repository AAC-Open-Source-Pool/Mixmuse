let subMenu = document.getElementById("sub");
        
function toggleMenu(){
    sub.classList.toggle("open-menu");
}



const jobs = [
    {
        title: "Singer",
        details: 
            "We are seeking a talented and experienced singer to join our team for live performances at various events and venues.",
        openPositions: "2",
        link: "#",
    },
    {
        title: "Guitarist",
        details: 
            "We are seeking a talented guitarist The ideal candidate will have a strong musical background, excellent technical skills, and the ability to adapt to different genres and styles.",
        openPositions: "3",
        link: "#",
    },
    {
        title: "Lyricist",
        details: 
            "The ideal candidate should have a strong background in writing lyrics, a keen sense of storytelling, and the ability to craft compelling and meaningful songs.",
        openPositions: "5",
        link: "#",
    },
    {
        title: "Singer",
        details: 
            "We are seeking a talented and experienced singer to join our team for live performances at various events and venues.",
        openPositions: "9",
        link: "#",
    },
    {
        title: "Singer",
        details: 
            "We are seeking a talented and experienced singer to join our team for live performances at various events and venues.",
        openPositions: "1",
        link: "#",
    },
    {
        title: "Guitarist",
        details: 
            "We are seeking a talented guitarist The ideal candidate will have a strong musical background, excellent technical skills, and the ability to adapt to different genres and styles.",
        openPositions: "3",
        link: "#",
    },
];

const jobsheading = document.querySelector(".job-list-container h2");

if(jobs.length == 1){
    jobsheading.innerHTML = `${jobs.length} Job`;
}
else{
    jobsheading.innerHTML = `${jobs.length} Jobs`;
}


const jobContainer = document.querySelector(".job-list-container .jobs");

const createCards = () => {
    jobs.forEach(job => {
        let jobCard = document.createElement("div");
        jobCard.classList.add("job");


        let title = document.createElement("h3");
        title.innerHTML = job.title;
        title.classList.add("job-title");

        let details = document.createElement("div");
        details.innerHTML = job.details;
        details.classList.add("details");

        let detailsbtn = document.createElement("a");
        detailsbtn.href = '../Requirments page/requirments.html';
        detailsbtn.innerHTML = "More Details";
        detailsbtn.classList.add("details-btn");

        let openPositions = document.createElement("span");
        openPositions.classList.add("open-positions");

        if(job.openPositions == 1){
            openPositions.innerHTML = `${job.openPositions} open position`;
        } else{
            openPositions.innerHTML = `${job.openPositions} open positions`;
        }


        jobCard.appendChild(title);
        jobCard.appendChild(details);
        jobCard.appendChild(detailsbtn);
        jobCard.appendChild(openPositions);

        jobContainer.appendChild(jobCard)
    });
};

createCards();
