# OOXML PresentationML Quick Reference

This reference documents Open Packaging Conventions (OPC) and PresentationML specifications required for surgical `.pptx` manipulation.

---

## 1. Package Architecture & Namespaces

A `.pptx` archive contains XML parts bound together by Relationship files (`.rels`).

### Core Namespaces
| Prefix | Namespace URI | Description |
|---|---|---|
| `p:` | `http://schemas.openxmlformats.org/presentationml/2006/main` | PresentationML elements (`<p:sp>`, `<p:pic>`, `<p:sldIdLst>`) |
| `a:` | `http://schemas.openxmlformats.org/drawingml/2006/main` | DrawingML primitives (`<a:p>`, `<a:r>`, `<a:t>`, `<a:xfrm>`) |
| `r:` | `http://schemas.openxmlformats.org/officeDocument/2006/relationships` | Attribute relationships (`r:id`, `r:embed`) |
| `rel:` | `http://schemas.openxmlformats.org/package/2006/relationships` | Package relationship definitions (`<Relationship>`) |
| `ct:` | `http://schemas.openxmlformats.org/package/2006/content-types` | Content-type registrations (`<Override>`, `<Default>`) |

---

## 2. Units & Coordinates (EMU)

PowerPoint uses **English Metric Units (EMU)** to represent all lengths, coordinates, and offsets without floating-point rounding errors:

$$	ext{1 inch} = 914,400	ext{ EMU}$$
$$	ext{1 cm} = 360,000	ext{ EMU}$$
$$	ext{1 pt} = 12,700	ext{ EMU}$$
$$	ext{1 px (at 96 DPI)} = 9,525	ext{ EMU}$$

### Standard Slide Dimensions
- **16:9 Widescreen**: $12,192,000 	imes 6,858,000	ext{ EMU}$ ($13.333" 	imes 7.5"$)
- **4:3 Standard**: $9,144,000 	imes 6,858,000	ext{ EMU}$ ($10.0" 	imes 7.5"$)

---

## 3. Shape Hierarchy (`<p:sp>`)

```xml
<p:sp>
  <!-- Non-visual properties: ID and Name -->
  <p:nvSpPr>
    <p:cNvPr id="201" name="Title Box"/>
    <p:cNvSpPr txBox="1"/>
    <p:nvPr/>
  </p:nvSpPr>
  
  <!-- Visual shape properties: Position, Size, Geometry, Fill, Stroke -->
  <p:spPr>
    <a:xfrm>
      <a:off x="914400" y="457200"/>   <!-- (1.0", 0.5") -->
      <a:ext cx="10363200" cy="914400"/> <!-- (11.33" x 1.0") -->
    </a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
    <a:solidFill><a:srgbClr val="0B1A2E"/></a:solidFill>
  </p:spPr>
  
  <!-- Text body -->
  <p:txBody>
    <a:bodyPr lIns="91440" tIns="91440" rIns="91440" bIns="91440"/>
    <a:p>
      <a:pPr algn="l"/>
      <a:r>
        <a:rPr sz="2400" b="1"><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill></a:rPr>
        <a:t>Executive Summary</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>
```

---

## 4. Text Hierarchy & Run Splitting

Visible sentences are often split into multiple `<a:r>` runs:
```xml
<a:p>
  <a:r><a:rPr b="1"/><a:t>AUC Score: </a:t></a:r>
  <a:r><a:rPr b="0"/><a:t>0.955 on standard benchmarks</a:t></a:r>
</a:p>
```
*Font sizes*: Stored in hundredths of a point (`sz="2400"` = 24pt, `sz="1400"` = 14pt).

### XML Escaping Mandatory
- `&` $ightarrow$ `&amp;`
- `<` $ightarrow$ `&lt;`
- `>` $ightarrow$ `&gt;`
- `"` $ightarrow$ `&quot;`
- `'` $ightarrow$ `&apos;`

---

## 5. Hyperlink Wiring

Changing visible text does NOT alter link destination.

1. **Slide XML**:
   ```xml
   <a:r>
     <a:rPr>
       <a:hlinkClick r:id="rId5"/>
     </a:rPr>
     <a:t>https://github.com/sparsh101sparsh/netra-deepfake-detector</a:t>
   </a:r>
   ```

2. **Slide Relationship (`ppt/slides/_rels/slideN.xml.rels`)**:
   ```xml
   <Relationship Id="rId5" 
     Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink" 
     Target="https://github.com/sparsh101sparsh/netra-deepfake-detector" 
     TargetMode="External"/>
   ```

---

## 6. Slide Order vs Filenames

`ppt/presentation.xml` `<p:sldIdLst>` dictates visual order:
```xml
<p:sldIdLst>
  <p:sldId id="256" r:id="rId8"/> <!-- Slide 1 -->
  <p:sldId id="257" r:id="rId9"/> <!-- Slide 2 -->
  <p:sldId id="260" r:id="rId12"/> <!-- Slide 3 (can point to slide8.xml!) -->
</p:sldIdLst>
```
Never infer slide order from `slide1.xml`, `slide2.xml` filenames.
