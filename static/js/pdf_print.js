document.addEventListener("DOMContentLoaded", () => {
  const downloadButton = document.getElementById("download-pdf");
  const contractElement = document.getElementById("contract-detail");

  if (downloadButton && contractElement) {
    downloadButton.addEventListener("click", generatePDF);
  } else {
    console.error(
      "Required elements not found. Check IDs: download-pdf, contract-detail"
    );
  }

  async function generatePDF() {
    try {
      downloadButton.disabled = true;
      downloadButton.textContent = "Generating PDF...";

      const pdfOptions = {
        margin: 10,
        filename: "contract.pdf",
        image: { type: "jpeg", quality: 0.98 },
        html2canvas: { scale: 2 },
        jsPDF: { unit: "mm", format: "a4", orientation: "portrait" },
      };

      const pdf = await html2pdf().from(contractElement).set(pdfOptions).save();

      console.log("PDF generated successfully");
    } catch (error) {
      console.error("Error generating PDF:", error);
      alert("Failed to generate PDF. Please try again.");
    } finally {
      downloadButton.disabled = false;
      downloadButton.textContent = "Download PDF";
    }
  }
});
