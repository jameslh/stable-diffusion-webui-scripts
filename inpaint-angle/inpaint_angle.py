import modules.scripts as scripts
import PIL


class Script(scripts.Script):
    def title(self):
        return "Inpaint Angle"

    def show(self, is_img2img):
        return is_img2img

    def ui(self, is_img2img):
        angle = gr.Number(value=0, label="Angle")
        return [angle]

    def run(self, p, angle):
        def im_crop_center(img, w, h):
            img_width, img_height = img.size
            left, right = (img_width - w) / 2, (img_width + w) / 2
            top, bottom = (img_height - h) / 2, (img_height + h) / 2
            left, top = round(max(0, left)), round(max(0, top))
            right, bottom = round(min(img_width - 0, right)
                                  ), round(min(img_height - 0, bottom))
            return img.crop((left, top, right, bottom))

        # Obtain the image size before reisizing occurs
        orig_width, orig_height = p.init_images[0].size

        # For non-zero angles, the image mask and all init_images will be rotated.
        # Rotations in PIL are counter-clockwise for positive angles.
        if angle != 0:
            if p.image_mask:
                p.image_mask = p.image_mask.rotate(
                    angle, expand=True, resample=PIL.Image.BICUBIC)
            for i in range(len(p.init_images)):
                p.init_images[i] = p.init_images[i].rotate(
                    angle, expand=True, resample=PIL.Image.BICUBIC)

        proc = process_images(p)

        # Reapply original image size by cropping to the center of the (potentially) expanded image.
        for i in range(len(proc.images)):
            proc.images[i] = im_crop_center(
                proc.images[i].rotate(-angle, expand=True, resample=PIL.Image.BICUBIC), orig_width, orig_height)

        return proc
