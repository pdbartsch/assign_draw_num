document.querySelectorAll("th.order").forEach((th_elem) => {
  let asc = true;
  const index = Array.from(th_elem.parentNode.children).indexOf(th_elem);
  th_elem.addEventListener("click", (e) => {
    const arr = [...th_elem.closest("table").querySelectorAll("tbody tr")];
    arr.sort((a, b) => {
      const a_val = a.children[index].innerText;
      const b_val = b.children[index].innerText;
      return asc ? a_val.localeCompare(b_val) : b_val.localeCompare(a_val);
    });
    arr.forEach((elem) => {
      th_elem.closest("table").querySelector("tbody").appendChild(elem);
    });
    asc = !asc;
  });
});
