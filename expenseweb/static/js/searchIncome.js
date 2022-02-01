const searchField = document.querySelector("#searchField");
const defaultTbody = document.querySelector('.defaultTbody');
const searchTbody = document.querySelector('.searchTbody');
const paginationUl = document.querySelector('.pagination');
searchTbody.style.display = "none";

searchField.addEventListener("keyup", (e) => {
    const searchValue = e.target.value;

    if (searchValue.trim().length > 0) {
        fetch('/income/search-incomes', {
            body: JSON.stringify({searchText: searchValue}),
            method:"POST"
        })
        .then(res => res.json())
        .then(data => {
            defaultTbody.style.display = "none";
            searchTbody.style.display = "";

            if (data.length === 0){
                searchTbody.innerHTML = `
                <tr>
                    <td colspan="4">No data</td>
                </tr>
                `
            } else {
                searchTbody.innerHTML = ""
                data.forEach(item => {
                    searchTbody.innerHTML += `
                    <tr>
                        <td>${ item.amount }</td>
                        <td>${ item.source }</td>
                        <td>${ item.description }</td>
                        <td>${ item.date }</td>
                        <td>
                            <a href="{% url 'edit-expense' expense.id %}" class='btn btn-secondary btn-sm'>Edit</a>
                        </td>
                    </tr>
                    `
                })
            }
        }); 
    } else {
        defaultTbody.style.display = "";
        searchTbody.style.display = "none";
    }

})