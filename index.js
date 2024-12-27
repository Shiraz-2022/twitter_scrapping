async function runScript() {
  try {
    const response = await fetch("http://localhost:5000/runscript", {
      method: "GET",
    });
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    const data = await response.json();

    if (data.trends && data.trend_data) {
      const dateValue = data.trend_data.date?.["$date"];
      document.getElementById("trend-date").innerText = dateValue
        ? new Date(dateValue).toLocaleString()
        : "No Date Available";

      document.getElementById("trend-list").innerHTML = data.trends
        .map((trend) => `<li>- ${trend}</li>`)
        .join("");
      document.getElementById(
        "ip-address"
      ).textContent = ` ${data.trend_data.ip_address}`;

      document.getElementById("json-data").textContent = JSON.stringify(
        data.trend_data,
        null,
        2
      );
    } else {
      console.error("Error in trends data:", data.error);
      alert("Data error", data.error);
    }
  } catch (error) {
    console.error("Error:", error);
    alert("Error", error);
  }
}

async function getTrends() {
  try {
    const response = await fetch("http://localhost:5000/gettrends", {
      method: "GET",
    });
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    const data = await response.json();

    if (data.trends) {
      document.getElementById("trend-list").innerHTML = data.trends
        .map((trend) => `<li>- ${trend}</li>`)
        .join("");

      document.getElementById("json-data").textContent = JSON.stringify(
        data,
        null,
        2
      );
    } else {
      console.error("Error fetching trends:", data.error);
    }
  } catch (error) {
    console.error("Error:", error);
    alert("An error occurred while fetching trends.");
  }
}
