        $(document).ready(function() {
            // Handle delete word form submission
            $('form[id^="delete-word-form-"]').submit(function(event) {
                event.preventDefault();
                var form = $(this);
                var url = form.attr('action');
                $.ajax({
                    url: url,
                    method: 'POST',
                    data: form.serialize(),
                    success: function(response) {
                        if (response.success) {
                            var wordId = form.attr('id').split('-')[3];
                            $('#word-' + wordId).remove();
                        }
                    },
                    error: function(response) {
                        console.log(response.responseText);
                    }
                });
            });

            // Handle edit word button click
            $('button.edit-word-btn').click(function() {
                var wordId = $(this).data('word-id');
                var wordText = $(this).data('word-text');
                var wordTranslation = $(this).data('word-translation');

                // Set the form values to the retrieved data
                $('#id_word').val(wordText);
                $('#id_translation').val(wordTranslation);

                // Update the form action with the word ID
                $('#edit-word-form').attr('action', '/edit_word/' + wordId + '/');

                // Display the modal with the form
                $('#edit-word-modal').modal('show');
            });

            // Handle edit word form submission
            $('#edit-word-form').submit(function(event) {
                event.preventDefault();
                var form = $(this);
                var url = form.attr('action');
                $.ajax({
                    url: url,
                    method: 'POST',
                    data: form.serialize(),
                    success: function(response) {
                        if (response.success) {
                            var wordId = url.split('/')[2];
                            var wordRow = $('#word-' + wordId);
                            console.log(wordRow);
                            wordRow.find('.word-text').text(response.word.word);
                            wordRow.find('.word-translation').text(response.word.translation);
                            $('#edit-word-modal').modal('hide');
                        }
                    },
                    error: function(response) {
                        console.log(response.responseText);
                    }
                });
            });
        });