$(function() {

    // PERFORM TRANSACTION AJAX FUNCTION
    $("#form-button").click(function(e) {
        // serialize form data
        const $serializedFormData = $("#transaction-form").serialize();

        $.post(
            "/customer-accounts/transaction",
            $serializedFormData,
        ).done(
            function (response) {
                //reset form fields and hide modal
                $("#transaction-form").trigger("reset")
                $("#transactionModal").modal("hide")

                // reload elements to update account balances
                $("#totalBalance").load(" #totalBalance")
                $("#customer_accounts").load(" #customer_accounts")
                $("#dataTable").load(" #dataTable")
                $("#transaction-totals").load(" #transaction-totals")
                $("#transactionChartjs").load(" #transactionChartjs")
                
                // $("#myChart").load(" #myChart")

                // Render messages
                if (response.data){
                    $("#dashboardAlerts").html(`
                    <div class="card bg-success text-white mb-4">
                        <div class="card-body">$${response.data.amount} ${response.data.transaction_type} </div>
                        <div class="card-footer d-flex align-items-center justify-content-between">
                            <a class="small text-white stretched-link" href="#">Success</a>
                            <div class="small text-white"><i class="fa fa-check-circle" aria-hidden="true"></i></div>
                        </div>
                    </div>
                `).show().fadeOut(10000)

                }
                else if (response.error){
                    $("#dashboardAlerts").html(`
                    <div class="card bg-danger text-white mb-4">
                        <div class="card-body">${response.error}</div>
                        <div class="card-footer d-flex align-items-center justify-content-between">
                            <a class="small text-white stretched-link" href="#">Error</a>
                            <div class="small text-white"><i class="fa fa-exclamation-circle" aria-hidden="true"></i></div>
                        </div>
                    </div>
                `).show().fadeOut(10000)
                }

            }
        )    
    })

    // ACCOUNT CREATION AJAX FUNCTION
    $("#create-account-form-button").click(function(e) {
        // serialize form data
        const $serializedFormData = $("#create-account-form").serialize();

        $.post(
            "/customer-accounts/create-account",
            $serializedFormData,
        ).done(
            function (response) {
                //reset form fields and hide modal
                $("#create-account-form").trigger("reset")
                $("#createAccountModal").modal("hide")
                
                // reload elements to update account balances
                $("#customer_accounts").load(" #customer_accounts")    

                // Render messages
                if (response.error){
                    $("#dashboardAlerts").html(`
                    <div class="card bg-danger text-white mb-4">
                        <div class="card-body">${response.error}</div>
                        <div class="card-footer d-flex align-items-center justify-content-between">
                            <a class="small text-white stretched-link" href="#">Error</a>
                            <div class="small text-white"><i class="fa fa-exclamation-circle" aria-hidden="true"></i></div>
                        </div>
                    </div>
                `).show().fadeOut(5000)

                } else if (response.success){
                    $("#dashboardAlerts").html(`
                    <div class="card bg-success text-white mb-4">
                        <div class="card-body">${response.success}</div>
                        <div class="card-footer d-flex align-items-center justify-content-between">
                            <a class="small text-white stretched-link" href="#">Success</a>
                            <div class="small text-white"><i class="fa fa-check-circle" aria-hidden="true"></i></div>
                        </div>
                    </div>
                    `).show().fadeOut(10000)
                }

                // reload buttons to apply conditionals when an account is created
                $("#accountButtons").load(" #accountButtons")
            }
         )    
    })

    // ACCOUNTS TRANSFER AJAX FUNCTION
    $("#accounts-transfer-form-button").click(function(e) {
        // serialize form data
        const $serializedFormData = $("#accounts-transfer-form").serialize();

        $.post(
            "/customer-accounts/accounts-funds-transfer",
            $serializedFormData,
        ).done(
            function (response) {
                //reset form fields and hide modal
                $("#accounts-transfer-form").trigger("reset")
                $("#accountsTransferModal").modal("hide")
                
                // reload elements to update account balances
                $("#customer_accounts").load(" #customer_accounts")    

                // Render messages
                if (response.error){
                    $("#dashboardAlerts").html(`
                    <div class="card bg-danger text-white mb-4">
                        <div class="card-body">${response.error}</div>
                        <div class="card-footer d-flex align-items-center justify-content-between">
                            <a class="small text-white stretched-link" href="#">Error</a>
                            <div class="small text-white"><i class="fa fa-exclamation-circle" aria-hidden="true"></i></div>
                        </div>
                    </div>
                `).show().fadeOut(10000)

                } else if (response.success){
                    $("#dashboardAlerts").html(`
                    <div class="card bg-success text-white mb-4">
                        <div class="card-body">${response.success}</div>
                        <div class="card-footer d-flex align-items-center justify-content-between">
                            <a class="small text-white stretched-link" href="#">Success</a>
                            <div class="small text-white"><i class="fa fa-check-circle" aria-hidden="true"></i></div>
                        </div>
                    </div>
                    `).show().fadeOut(10000)
                }
            }
         )    
    })
    
})