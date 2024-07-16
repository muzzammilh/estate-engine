document.getElementById("download-pdf").addEventListener("click", function () {
  var element = document.getElementById("contract-detail");
  console.log(element); // Check if element is selected correctly
  if (element) {
    html2pdf().from(element).save();
  } else {
    console.error("Element with ID 'contract-detail' not found.");
  }
});
