// custom javascript
$( document ).ready(() => {
  console.log('Sanity Check!');
	$('.btn').on('click', function() {
	  $('#spinner').toggle();
	  $.ajax({
	    url: 'http://localhost:8000/create',
	    method: 'POST',
	    contentType: 'application/json',
	    data: JSON.stringify({ 'number': $(this).data('type') }),
	  })
	  .done((res) => {
	    getStatus(res.data.task_id)
	  })
	  .fail((err) => {
	    console.log(err)
	  });
	});

	function getStatus(taskID) {
	  $.ajax({
            url: `http://localhost:8000/status/${taskID}`,
	    method: 'GET'
	  })
	  .done((res) => {
	    const html = `
	      <tr id='${res.task_id}'>
		<td>${res.task_id}</td>
		<td id='status'>${res.status}</td>
		<td id='result'>${res.result}</td>
	      </tr>`

	
	    if ($("#tasks").find(`#${res.task_id}`).length > 0) {
	       $(`#${res.task_id}`).replaceWith(html);
	    } else {
	    	$('#tasks').prepend(html);
	    }

	    const taskStatus = res.status;
	    if (taskStatus === 'SUCCESS' || taskStatus === 'FAILED') 
		  return false;

	    setTimeout(function() {
	      getStatus(res.task_id);
	    }, 1000);
	  })
	  .fail((err) => {
	    console.log(err)
	  });
	}
});
