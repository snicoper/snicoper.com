/**
 * Carga una imagen de un input type file para mostrarla
 * en un elemento <img>
 * @param  {str} $idTagImage id en la etiqueta <img id=""> '#my-id-tag'.
 * @param  {str} input       Elemento del input.
 *
 * $("#id_avatar").change(function(){
 *   readImagePreview('#img-avatar', this);
 * });
 *
 * #id_avatar es el campo type field.
 * #img-avatar es el id del elemento <img>
 */
function readImagePreview ($idTagImage, input) { // eslint-disable-line no-unused-vars
  const reader = new FileReader();

  if (input.files && input.files[0]) {
    reader.onload = function (e) {
      $($idTagImage).attr('src', e.target.result);
    };
    reader.readAsDataURL(input.files[0]);
  }
}
