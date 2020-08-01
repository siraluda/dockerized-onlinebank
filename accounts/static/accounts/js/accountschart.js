
let myChart = document.getElementById("transactionsChart").getContext('2d');
const transactionData = JSON.parse(document.getElementById("transaction-totals").textContent);

let tCHart = new Chart(myChart, {
    type: 'pie',
    data: {
        labels: ['Withdrawals', 'Deposits'],
        datasets: [{
            label: 'Amount',
            data:[
                transactionData.total_withdrawal,
                transactionData.total_deposit,
            ],
            backgroundColor: ['#ff7675', '#74b9ff'],
            borderWidth: 1
        }],
    },
    options: {
        title: {
            display: true,
            text:'Expense tracker',
        }
    },
})