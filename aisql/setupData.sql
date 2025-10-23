-- Source
INSERT INTO Source (source_id, source_name, source_type, website_url) VALUES
(1, 'Nurilounge', 'App', 'https://www.nurilounge.com/'),
(2, 'Pickple', 'Website', 'https://pickple.co/'),
(3, 'Statusphere', 'Website', 'https://www.statusphere.com/'),
(4, 'Stack', 'App', 'https://stackinfluence.com/'),
(5, 'Picky', 'App', 'https://www.picky.com/'),
(6, 'Shared Link', 'Form', NULL);

-- Brand
INSERT INTO Brand (brand_id, brand_name, brand_country, contact_email, website_url) VALUES
(1, 'Abib', 'Korea', NULL, 'https://en.abib.com/'),
(2, 'Thayers', 'EUSA', NULL, 'https://www.thayers.com/'),
(3, 'Lador', 'Korea', NULL, 'https://en.lador.co.kr/'),
(4, 'SKIN1004', 'Korea', NULL, 'https://www.skin1004.com/'),
(5, 'Medicube', 'Korea', NULL, 'https://www.medicube.com/'),
(6, 'Dinto', 'Korea', NULL, 'https://www.dinto.com/'),
(7, 'Biodance', 'Korea', NULL, 'https://www.biodance.com/'),
(8, 'Morphe', 'USA', NULL, 'https://www.morphe.com/'),
(9, 'ilso Global', 'Korea', 'tfairbank@milip.kr', 'https://theilso.com/index.html'),
(10, 'Bubble', 'USA', NULL, 'https://www.bubble.com/'),
(11, 'Neutrogena', 'USA', NULL, 'https://www.neutrogena.com/');

-- Category
INSERT INTO Category (category_id, category_name) VALUES
(100, 'Skincare'),
(101, 'Haircare'),
(102, 'Clothing'),
(103, 'Makeup'),
(104, 'Accessories');

-- BrandCategory
INSERT INTO BrandCategory (brand_id, category_id) VALUES
(1, 100),
(2, 100),
(3, 101),
(4, 100),
(5, 100),
(6, 103),
(7, 100),
(8, 103),
(9, 100),
(10, 100),
(11, 100);

-- Collaboration
INSERT INTO Collaboration (collaboration_id, brand_id, source_id, application_link, collaboration_type, application_date, approval_date, collaboration_status) VALUES
(1, 1, 2, 'No applicable', 'Product Review', '2025-07-01', '2025-07-10', 'Approved'),
(2, 2, 6, 'https://ambassadors.thayers.com/sign-up', 'Ambassador', '2025-07-15', '2025-07-20', 'Approved'),
(3, 3, 6, 'https://docs.google.com/forms/d/e/1FAIpQLSfdKK16sjBLxwxEMZyI6UVgeeylPjDXl96iG0DfyNiDFD8JLA/viewform?utm_id=120228266552180519&fbclid=PAQ0xDSwMDBSlleHRuA2FlbQIxMAABp5IaMtYgvAq3xV6reRshaZvJOEWwq4-3FLkfvY_gM3CVFf2nhl6fuSdsbyhD_aem_NUG4mcWE2tDlVZD8wBbw5Q', 'Product Review', '2025-08-01', '2025-08-05', 'Approved'),
(4, 4, 5, 'https://docs.google.com/forms/d/e/1FAIpQLSf5jjn6UY8B_arjbC7fwHYDHBCqMMJ4HtN-o3mbIl0PfzvPTw/viewform?fbclid=PAQ0xDSwMHQkRleHRuA2FlbQIxMAABpysr6bCsygoDTz0r6EJs6LHPF6OnPqzWqgYu4vAnB8VcQszb9GbU4KYX-F8W_aem_Cd-7W-O7BJRXcIYnC0X8Hw', 'Product Review', '2025-09-10', NULL, 'Declined'),
(5, 5, 6, 'https://socialladder.rkiapps.com/medicube/application/applynow', 'Ambassador', '2025-08-01', NULL, 'Declined'),
(6, 6, 1, 'No applicable', 'Product Review', '2025-07-30', '2025-08-10', 'Approved'),
(7, 4, 6, 'No applicable','Product Review', '2025-07-16', '2025-07-25', 'Approved'),
(8, 7, 6, 'https://docs.google.com/forms/d/e/1FAIpQLSfxoyxBbRDETJ74M5tbbVRsJDnDabAILZ1p1JW1ya8TT4xtPg/viewform?fbclid=PAQ0xDSwLmkwZleHRuA2FlbQIxMAABp-S2xqjvNb_EhlHxcD3heuAjO1i3Lj9W3OelTnbLHXGYJOrDhBdWkTVkYeGj_aem_98DIs5Kcyfyqu-yBpytk8Q', 'Product Review', '2025-08-07', '2025-08-21', 'Approved'),
(9, 8, 6, NULL, 'Product Review', '2025-07-24', NULL, 'Approved'),
(10, 9, 6, NULL, 'Product Review', '2025-07-02', NULL, 'Approved'),
(11, 10, 6, 'https://hellobubble.com/pages/college-ambassadors?srsltid=AfmBOorfPcuPJldYbYQ3st8E9g26coU6yTFXzeImCRoEuHzeyi3wrCAD', 'Ambassador', '2025-09-05', NULL, 'Approved'),
(12, 11, 3, 'No applicable', 'Product Review', '2025-09-16', '2025-09-20', 'Approved');


-- Product
INSERT INTO Product (product_id, collaboration_id, product_name, product_status, received_date) VALUES
(1, 1, 'Airy Sunstick', 'Received', '2025-07-20'),
(2, 2, 'Rose Petal Toner', 'Received', '2025-08-07'),
(3, 3, 'Hair Oil', 'Received', '2025-08-21'),
(4, 6, '3 Glowy Lip Tint', 'Received', '2025-08-22'),
(5, 7, 'Tea trica products', 'Received', '2025-08-01'),
(6, 8, 'Collagen Jelly Pad', 'Received', '2025-09-03'),
(7, 9, 'Blush Set + Eyeshadow Brushes', 'Received', '2025-08-18'),
(8, 10, 'Hydrating Serum', 'Received', '2025-07-30'),
(9, 11, 'Skincare Set', 'Received', '2025-09-26'),
(10, 12, 'Travel Skincare Set', 'Received', '2025-09-29');

-- ContentRequirement
INSERT INTO ContentRequirement (requirement_id, product_id, content_type, platform, deadline, content_url) VALUES
(1, 1, 'Video', 'Tiktok', '2025-09-15', 'https://piktok.io/index/dispWp_picktalkCampaignDetail?product_srl=94087'),
(2, 2, 'Video', 'Instagram', '2025-08-15', 'No applicable'),
(3, 3, 'Video', 'Tiktok', '2025-10-20', 'No applicable'),
(4, 4, 'Video', 'Instagram', '2025-09-10', 'https://nurilounge.notion.site/Dinto-Blur-glowy-lip-tint-Content-Guidelines-1de9439ada93804dad50d85a32609850'),
(5, 5, 'Video', 'Instagram', '2025-08-20', NULL),
(6, 6, 'Video', 'Instagram', '2025-09-20', 'No applicable'),
(7, 7, 'Video', 'Instagram', '2025-10-01', 'No applicable'),
(8, 9, 'Video', 'Instagram', '2025-10-10', 'No applicable'),
(9, 10, 'Video', 'Instagram', '2025-10-06', 'No applicable');

-- ContentStatus
INSERT INTO ContentStatus (status_id, requirement_id, content_status, start_date, completed_date) VALUES
(1, 1, 'Completed', '2025-09-12', '2025-09-14'),
(2, 2, 'Not Started', NULL, NULL),
(3, 3, 'Completed', '2025-10-09', '2025-10-12'),
(4, 4, 'Completed', '2025-09-02', '2025-09-06'),
(5, 5, 'Completed', '2025-08-15', '2025-08-18'),
(6, 6, 'Completed', '2025-09-10', '2025-09-15'),
(7, 7, 'Not Started', NULL, NULL),
(8, 8, 'Not Started', NULL, NULL),
(9, 9, 'Completed', '2025-10-05', '2025-10-06');


-- Compensation
INSERT INTO Compensation (compensation_id, status_id, collaboration_id, compensation_type, amount, received_date, compensation_status) VALUES
(1, 1, 1, 'App Payment', 20, '2025-09-25', 'Completed'),
(2, 3, 3, 'App Payment', 15, '2025-10-28', 'Completed'),
(3, 4, 6, 'Paypal', 3, '2025-09-17', 'Completed'),
(4, 5, 7, 'App Payment', 5, '2025-09-15', 'Completed'),
(5, 6, 8, 'No compensation', 0, NULL, NULL),
(6, 9, 12, 'Gift Card', 50, '2025-10-12', 'Completed');
