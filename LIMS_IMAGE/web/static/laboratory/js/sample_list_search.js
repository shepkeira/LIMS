const sampleList = document.getElementsByClassName("list-group");
const searchInput = document.querySelector("#search");

// Add event listener to search input field to filter the list of samples on keyup
searchInput.addEventListener("keyup", function () {
  const searchValue = searchInput.value.toLowerCase();
  for (let i = 0; i < sampleList.length; i++) {
    const sample = sampleList[i].getElementsByClassName("list-group-item")[0];
    // If the sample name contains the search value, show the sample
    if (sample.innerText.toLowerCase().indexOf(searchValue) > -1) {
      sampleList[i].style.display = "";
    } else {
      sampleList[i].style.display = "none";
    }
  }
});
