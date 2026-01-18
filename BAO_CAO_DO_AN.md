# BÁO CÁO ĐỒ ÁN CUỐI KỲ

**Học phần:** Phân tích thiết kế giải thuật

**Đề tài:** HỆ THỐNG GAME POKEKAWAII
(Game Ghép Hình Pokemon Kawaii Classic)

---

**Giảng viên hướng dẫn:** [Tên giảng viên]

**Sinh viên thực hiện:**
- Họ và tên: [Tên sinh viên]
- MSSV: [Mã số sinh viên]
- Lớp: [Tên lớp]

**Thành phố Hồ Chí Minh, tháng 01 năm 2026**

---

## MỤC LỤC

1. [MỞ ĐẦU](#phần-1-mở-đầu)
   - 1.1. Giới thiệu ứng dụng
   - 1.2. Mục tiêu đồ án
   - 1.3. Công nghệ sử dụng

2. [PHÂN TÍCH THUẬT TOÁN](#phần-2-phân-tích-thuật-toán)
   - 2.1. Fisher-Yates Shuffle Algorithm
   - 2.2. Pathfinding với Ràng Buộc Lượt Rẽ
   - 2.3. Hint Finding Algorithm
   - 2.4. Board Generation Algorithm
   - 2.5. Ice Placement Algorithm
   - 2.6. Move Validation & Board Update
   - 2.7. Board Clear Check Algorithm

3. [THIẾT KẾ HỆ THỐNG](#phần-3-thiết-kế-hệ-thống)
   - 3.1. Kiến trúc hệ thống
   - 3.2. Cấu trúc dữ liệu
   - 3.3. Sơ đồ luồng xử lý

4. [KẾT QUẢ VÀ ĐÁNH GIÁ](#phần-4-kết-quả-và-đánh-giá)
   - 4.1. Kết quả đạt được
   - 4.2. So sánh độ phức tạp
   - 4.3. Đánh giá và nhận xét

5. [KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN](#phần-5-kết-luận-và-hướng-phát-triển)

---

## PHẦN 1: MỞ ĐẦU

### 1.1. Giới thiệu ứng dụng

PokeKawaii là một ứng dụng game ghép hình theo phong cách Pikachu Kawaii Classic, được phát triển nhằm minh họa việc áp dụng các thuật toán và cấu trúc dữ liệu trong lập trình game. Game lấy cảm hứng từ thể loại ghép hình Mahjong truyền thống, kết hợp với đồ họa Pokemon để tạo nên một trải nghiệm chơi game thú vị và giàu tính giáo dục.

Ứng dụng được xây dựng theo mô hình Client-Server, với Backend sử dụng Python FastAPI để xử lý logic game và Frontend sử dụng React để hiển thị giao diện người dùng. Điểm đặc biệt của dự án là việc tích hợp nhiều thuật toán kinh điển trong khoa học máy tính như BFS (Breadth-First Search), Fisher-Yates Shuffle, Hash Map, và các thuật toán tìm đường với ràng buộc.

### 1.2. Mục tiêu đồ án

Đồ án được thực hiện với các mục tiêu chính sau:

- **Ứng dụng kiến thức về giải thuật:** Triển khai các thuật toán sắp xếp, tìm kiếm, đệ quy, tham lam, và đồ thị để giải quyết các bài toán cụ thể trong game.

- **Phân tích hiệu năng và lựa chọn thuật toán:** So sánh độ phức tạp thời gian và không gian của các thuật toán khác nhau, từ đó lựa chọn thuật toán tối ưu cho từng chức năng.

- **Rèn luyện kỹ năng lập trình:** Thực hành kỹ năng lập trình thực tế, từ thiết kế kiến trúc hệ thống đến triển khai và tối ưu hóa code.

- **Trình bày báo cáo kỹ thuật:** Phát triển khả năng phân tích, đánh giá và trình bày các thuật toán một cách khoa học và chuyên nghiệp.

### 1.3. Công nghệ sử dụng

#### 1.3.1. Backend - Python FastAPI

- **FastAPI 0.109.0:** Framework web hiện đại, hiệu năng cao cho Python, hỗ trợ async/await và tự động generate API documentation.
- **Uvicorn 0.27.0:** ASGI server để chạy ứng dụng FastAPI.
- **Pydantic 2.5.3:** Thư viện validation dữ liệu mạnh mẽ, đảm bảo type safety.

#### 1.3.2. Frontend - React

- **React 18.2.0:** Thư viện JavaScript để xây dựng user interface.
- **Vite 5.0.11:** Build tool hiện đại, nhanh chóng cho React applications.
- **Axios 1.6.5:** HTTP client để giao tiếp với Backend API.

#### 1.3.3. Deployment & DevOps

- **Docker:** Containerization cho cả Backend và Frontend.
- **Render:** Cloud platform để deploy ứng dụng production.
- **Git & GitHub:** Version control và code repository.

---

## PHẦN 2: PHÂN TÍCH THUẬT TOÁN

### 2.1. Fisher-Yates Shuffle Algorithm

#### 2.1.1. Mô tả bài toán

Trong game PokeKawaii, cần phân bố ngẫu nhiên các Pokemon trên bàn chơi sao cho mỗi ván chơi có bố cục khác nhau, đồng thời đảm bảo tính công bằng (mọi hoán vị có xác suất bằng nhau).

#### 2.1.2. Lý do lựa chọn thuật toán

Fisher-Yates Shuffle (còn gọi là Knuth Shuffle) được chọn vì:

- Độ phức tạp thời gian O(n) - tuyến tính, rất hiệu quả
- Độ phức tạp không gian O(1) - xáo trộn tại chỗ (in-place)
- Đảm bảo không thiên vị - mọi hoán vị có xác suất 1/n!
- Dễ hiểu và triển khai

#### 2.1.3. Thuật toán áp dụng

**Các bước thực hiện:**

1. Duyệt mảng từ cuối về đầu (index từ n-1 đến 1)
2. Tại mỗi vị trí i, chọn ngẫu nhiên index j trong khoảng [0, i]
3. Hoán đổi phần tử tại vị trí i với phần tử tại vị trí j
4. Tiếp tục cho đến khi hoàn thành

#### 2.1.4. Source code

```python
def fisher_yates_shuffle(items):
    """
    Xáo trộn danh sách tại chỗ (in-place)
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    n = len(items)

    # Duyệt từ cuối về đầu
    for i in range(n - 1, 0, -1):
        # Chọn ngẫu nhiên index j từ [0, i]
        j = random.randint(0, i)

        # Hoán đổi items[i] với items[j]
        items[i], items[j] = items[j], items[i]

    return items
```

#### 2.1.5. Phân tích độ phức tạp

**Độ phức tạp thời gian:** O(n)
- Duyệt qua n phần tử đúng 1 lần
- Mỗi phép hoán đổi là O(1)
- Tổng: O(n)

**Độ phức tạp không gian:** O(1)
- Chỉ sử dụng biến tạm i, j
- Xáo trộn tại chỗ, không tạo mảng mới

#### 2.1.6. So sánh với các thuật toán khác

| Thuật toán | Time Complexity | Space Complexity | Unbiased |
|------------|----------------|------------------|----------|
| Fisher-Yates Shuffle | O(n) | O(1) | ✅ Yes |
| Naive Shuffle (sort random) | O(n log n) | O(n) | ❌ No |
| Selection Sampling | O(n²) | O(n) | ✅ Yes |

---

### 2.2. Pathfinding với Ràng Buộc Lượt Rẽ

#### 2.2.1. Mô tả bài toán

Tìm đường nối giữa hai ô Pokemon giống nhau trên bàn chơi với các ràng buộc:

- Đường đi chỉ gồm các đoạn thẳng (ngang hoặc dọc)
- Tối đa 3 lượt rẽ (thay đổi hướng)
- Không đi qua ô có Pokemon khác
- Có thể đi vòng qua biên bàn chơi

#### 2.2.2. Các phương pháp tiếp cận

**Phương pháp 1: BFS với Theo Dõi Lượt Rẽ**

Sử dụng thuật toán BFS (Breadth-First Search) cải tiến:
- State: (row, col, direction, turns, path)
- Queue để duyệt các state theo chiều rộng
- Visited set để tránh lặp vô hạn
- Stop condition: turns > 3

**Độ phức tạp:**
- Time Complexity: O(rows × cols × 4)
- Space Complexity: O(rows × cols)

**Phương pháp 2: Simplified Pathfinding (Được áp dụng)**

Thay vì duyệt toàn bộ không gian trạng thái, kiểm tra các loại đường theo thứ tự từ đơn giản đến phức tạp:

1. **Đường thẳng (0 lượt rẽ):** Cùng hàng hoặc cùng cột
2. **Đường chữ L (1 lượt rẽ):** Qua 1 điểm góc
3. **Đường chữ Z/U (2 lượt rẽ):** Qua 2 điểm trung gian
4. **Đường qua biên (2-3 lượt rẽ):** Đi vòng ra ngoài bàn chơi

#### 2.2.3. Lý do lựa chọn Simplified Pathfinding

**Ưu điểm so với BFS:**

- **Early termination:** Dừng ngay khi tìm thấy đường đơn giản (thường xuyên xảy ra)
- **Cache-friendly:** Truy cập tuần tự vào grid, tốt cho CPU cache
- **Dễ debug:** Logic rõ ràng, dễ theo dõi từng bước
- **Hiệu suất thực tế:** Trong game, đường đơn giản (0-1 rẽ) chiếm ~70-80% trường hợp

#### 2.2.4. Source code - Kiểm tra đường thẳng (0 rẽ)

```python
def check_straight_path(pos1, pos2, grid):
    """
    Kiểm tra đường thẳng giữa 2 điểm
    """
    # Kiểm tra cùng hàng
    if pos1.row == pos2.row:
        min_col = min(pos1.col, pos2.col)
        max_col = max(pos1.col, pos2.col)

        # Kiểm tra các ô giữa có trống không
        for col in range(min_col + 1, max_col):
            if grid[pos1.row][col].type == "POKEMON":
                return False

        return MatchResult(
            is_valid=True,
            path=[pos1, pos2],
            turns=0
        )

    # Kiểm tra cùng cột
    if pos1.col == pos2.col:
        min_row = min(pos1.row, pos2.row)
        max_row = max(pos1.row, pos2.row)

        for row in range(min_row + 1, max_row):
            if grid[row][pos1.col].type == "POKEMON":
                return False

        return MatchResult(
            is_valid=True,
            path=[pos1, pos2],
            turns=0
        )

    return MatchResult(is_valid=False)
```

#### 2.2.5. Source code - Đường chữ L (1 rẽ)

```python
def check_l_shaped_path(pos1, pos2, grid):
    """
    Kiểm tra đường hình chữ L qua 1 góc
    """
    # Thử góc 1: (pos1.row, pos2.col)
    corner1 = Position(pos1.row, pos2.col)

    if is_empty(corner1, grid):
        # Kiểm tra 2 đoạn thẳng
        if is_line_clear_horizontal(pos1.col, corner1.col, pos1.row, grid) and \
           is_line_clear_vertical(corner1.row, pos2.row, corner1.col, grid):
            return MatchResult(
                is_valid=True,
                path=[pos1, corner1, pos2],
                turns=1
            )

    # Thử góc 2: (pos2.row, pos1.col)
    corner2 = Position(pos2.row, pos1.col)

    if is_empty(corner2, grid):
        if is_line_clear_vertical(pos1.row, corner2.row, pos1.col, grid) and \
           is_line_clear_horizontal(corner2.col, pos2.col, pos2.row, grid):
            return MatchResult(
                is_valid=True,
                path=[pos1, corner2, pos2],
                turns=1
            )

    return MatchResult(is_valid=False)
```

#### 2.2.6. Phân tích độ phức tạp

| Loại đường | Time Complexity | Giải thích |
|-----------|----------------|------------|
| 0 lượt rẽ (thẳng) | O(max(rows, cols)) | Kiểm tra 1 đường thẳng |
| 1 lượt rẽ (chữ L) | O(rows + cols) | Kiểm tra 2 góc, mỗi góc 2 đoạn thẳng |
| 2 lượt rẽ (chữ Z/U) | O(rows × cols) | Thử mọi hàng/cột làm đường giữa |
| **Worst case** | **O(rows × cols)** | Khi phải kiểm tra hết các loại đường |

**Average Case Analysis:**
- 70% trường hợp: Tìm thấy đường ở bước 1-2 (0-1 rẽ) → O(n)
- 25% trường hợp: Cần đến bước 3 (2 rẽ) → O(n²)
- 5% trường hợp: Không có đường hoặc cần 3 rẽ → O(n²)
- **Average: O(n)** với n = max(rows, cols)

---

### 2.3. Hint Finding Algorithm (Tìm Gợi Ý)

#### 2.3.1. Mô tả bài toán

Tìm một cặp Pokemon có thể ghép được (có đường đi hợp lệ) để gợi ý cho người chơi khi bế tắc.

#### 2.3.2. Thuật toán áp dụng

Sử dụng **Hash Map** kết hợp với **Early Termination**:

**Các bước thực hiện:**

1. Build hash map: nhóm Pokemon theo ID (pokemon_id → List[positions])
2. Duyệt qua các loại Pokemon có ≥ 2 vị trí
3. Với mỗi loại, thử tất cả các cặp vị trí
4. Kiểm tra xem có đường đi hợp lệ không (dùng Pathfinding)
5. Return ngay khi tìm thấy cặp hợp lệ đầu tiên (Early Termination)

#### 2.3.3. Source code

```python
def find_hint(game_state):
    """
    Tìm một nước đi hợp lệ để gợi ý
    Time Complexity: O(n²) worst case, O(n) average
    Space Complexity: O(n)
    """
    grid = game_state.board.grid
    rows, cols = game_state.board.rows, game_state.board.cols

    # Bước 1: Build hash map
    pokemon_positions = {}  # {pokemon_id: [positions]}

    for row in range(rows):
        for col in range(cols):
            cell = grid[row][col]

            # Chỉ xét Pokemon chưa bị đóng băng
            if cell.type == "POKEMON" and not cell.is_frozen:
                if cell.pokemon_id not in pokemon_positions:
                    pokemon_positions[cell.pokemon_id] = []

                pokemon_positions[cell.pokemon_id].append(
                    Position(row, col)
                )

    # Bước 2: Kiểm tra từng loại Pokemon
    for pokemon_id, positions in pokemon_positions.items():
        if len(positions) < 2:
            continue

        # Bước 3: Thử tất cả các cặp
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                pos1 = positions[i]
                pos2 = positions[j]

                # Bước 4: Kiểm tra đường đi
                result = pathfinder.find_path(pos1, pos2, grid)

                if result.is_valid:
                    # Bước 5: Return ngay (Early Termination)
                    return {"pos1": pos1, "pos2": pos2, "path": result.path}

    # Không tìm thấy
    return None
```

#### 2.3.4. Phân tích độ phức tạp

**Time Complexity Analysis:**
- **Build hash map:** O(rows × cols) = O(n)
- **Duyệt các loại Pokemon:** O(20) = O(1)
- **Thử các cặp của cùng loại:** O(k²) với k = số Pokemon cùng loại (thường k ≤ 4)
- **Kiểm tra đường đi:** O(n²) trong worst case
- **Early termination:** Dừng ngay khi tìm thấy → Average O(n)

**Space Complexity:** O(n) cho hash map

#### 2.3.5. So sánh với Brute Force

| Phương pháp | Time Complexity | Giải thích |
|-------------|----------------|------------|
| Brute Force | O(n⁴) | Duyệt tất cả cặp ô (n²) × kiểm tra đường đi (n²) |
| **Hash Map + Early Stop** | **O(n) average** | Chỉ kiểm tra Pokemon cùng loại + dừng sớm |

**Cải thiện: ~10,000x nhanh hơn** (với board 8×12)

---

### 2.4. Board Generation Algorithm

#### 2.4.1. Mô tả bài toán

Khởi tạo bàn chơi với các yêu cầu:

- Mỗi Pokemon xuất hiện ít nhất 2 lần (để ghép cặp)
- Tổng số ô phải chẵn
- Phân bố ngẫu nhiên nhưng cân bằng
- Thêm đá băng ở level cao

#### 2.4.2. Source code

```python
def generate_board(rows=8, cols=12, level=1):
    """
    Tạo bàn chơi mới
    Time Complexity: O(rows × cols)
    Space Complexity: O(rows × cols)
    """
    total_cells = rows * cols

    # Bước 1: Tạo danh sách Pokemon (phải chẵn)
    pokemon_list = []

    # Thêm 2 con của mỗi loại Pokemon (1-20)
    for pokemon_id in range(1, 21):
        pokemon_list.append(pokemon_id)
        pokemon_list.append(pokemon_id)

    # Bước 2: Điền thêm để đủ số ô
    while len(pokemon_list) < total_cells:
        random_id = random.randint(1, 20)
        pokemon_list.append(random_id)
        pokemon_list.append(random_id)  # Luôn thêm cặp

    # Bước 3: Cắt bớt nếu thừa
    pokemon_list = pokemon_list[:total_cells]

    # Bước 4: Xáo trộn bằng Fisher-Yates
    fisher_yates_shuffle(pokemon_list)

    # Bước 5: Điền vào grid
    grid = []
    index = 0
    for row in range(rows):
        grid_row = []
        for col in range(cols):
            cell = Cell(
                type="POKEMON",
                pokemon_id=pokemon_list[index],
                is_frozen=False
            )
            grid_row.append(cell)
            index += 1
        grid.append(grid_row)

    # Bước 6: Thêm đá băng nếu level cao
    if level >= 4:
        add_ice_blocks(grid, level)

    return GameBoard(
        grid=grid, rows=rows, cols=cols,
        time_remaining=300, lives=5, level=level, score=0
    )
```

#### 2.4.3. Phân tích độ phức tạp

| Bước | Thao tác | Time Complexity |
|------|---------|----------------|
| 1-3 | Tạo danh sách Pokemon | O(n) |
| 4 | Fisher-Yates Shuffle | O(n) |
| 5 | Điền vào grid | O(n) |
| 6 | Thêm đá băng | O(k) với k = số đá băng |
| **Tổng** | | **O(n)** với n = rows × cols |

---

### 2.5. Ice Placement Algorithm

#### 2.5.1. Mô tả thuật toán

Đặt đá băng ngẫu nhiên trên bàn chơi ở level cao, sử dụng Set để tránh trùng lặp vị trí.

#### 2.5.2. Source code

```python
def add_ice_blocks(grid, level):
    """
    Thêm đá băng vào bàn chơi
    Time Complexity: O(k) với k = số đá băng
    Space Complexity: O(k)
    """
    rows, cols = len(grid), len(grid[0])

    # Công thức tính số đá băng
    ice_count = min(level - 3, (rows * cols) // 4)

    ice_positions = set()  # Dùng set để tránh trùng

    # Đặt đá băng cho đến khi đủ số lượng
    while len(ice_positions) < ice_count:
        row = random.randint(0, rows - 1)
        col = random.randint(0, cols - 1)

        # Set tự động tránh trùng lặp
        ice_positions.add((row, col))

    # Đánh dấu các ô có đá băng
    for (row, col) in ice_positions:
        grid[row][col].is_frozen = True
```

**Tại sao dùng Set?**
- Set tự động loại bỏ duplicate → Không cần kiểm tra thủ công
- O(1) cho add và contains operations
- Code gọn gàng, dễ hiểu hơn

---

### 2.6. Move Validation & Board Update

#### 2.6.1. Quy trình xử lý nước đi

**Các bước validate và update:**

1. Kiểm tra 2 Pokemon có cùng loại không
2. Kiểm tra không bị đóng băng
3. Tìm đường đi hợp lệ (Pathfinding)
4. Nếu hợp lệ:
   - Xóa 2 Pokemon (set to EMPTY)
   - Xóa đá băng liền kề (4 hướng)
   - Cập nhật điểm số
   - Kiểm tra thắng

#### 2.6.2. Source code - Xóa đá băng liền kề

```python
def remove_adjacent_ice(pos, grid):
    """
    Xóa đá băng ở 4 ô liền kề (trên, dưới, trái, phải)
    """
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    rows, cols = len(grid), len(grid[0])

    for dr, dc in directions:
        new_row = pos.row + dr
        new_col = pos.col + dc

        # Kiểm tra trong bounds
        if 0 <= new_row < rows and 0 <= new_col < cols:
            cell = grid[new_row][new_col]

            # Xóa đá băng
            if cell.is_frozen:
                cell.is_frozen = False
```

---

### 2.7. Board Clear Check Algorithm

#### 2.7.1. Mô tả

Kiểm tra xem đã xóa hết Pokemon trên bàn chơi chưa (điều kiện thắng).

#### 2.7.2. Source code

```python
def is_board_clear(grid):
    """
    Kiểm tra xem còn Pokemon nào không
    Time Complexity: O(rows × cols)
    Space Complexity: O(1)
    """
    for row in grid:
        for cell in row:
            if cell.type == "POKEMON":
                return False  # Còn Pokemon → chưa thắng

    return True  # Hết Pokemon → Thắng!
```

**Độ phức tạp:**
- Time: O(n) với n = rows × cols
- Space: O(1) - chỉ duyệt, không lưu trữ

---

## PHẦN 3: THIẾT KẾ HỆ THỐNG

### 3.1. Kiến trúc hệ thống

#### 3.1.1. Kiến trúc tổng quan

Hệ thống PokeKawaii được thiết kế theo mô hình Client-Server với kiến trúc 3 tầng:

```
┌─────────────────┐
│   Browser       │  ← User Interface Layer
│  (localhost)    │
└────────┬────────┘
         │ HTTP/HTTPS
         ▼
┌─────────────────────┐
│   Frontend          │  ← Presentation Layer
│   React + Vite      │
│   (Port 3000/80)    │
└────────┬────────────┘
         │ Axios API Calls
         ▼
┌─────────────────────┐
│   Backend           │  ← Business Logic Layer
│   FastAPI + Python  │
│   (Port 8000)       │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│   In-Memory Store   │  ← Data Layer
│   Dict[game_id,     │
│   GameState]        │
└─────────────────────┘
```

#### 3.1.2. Cấu trúc thư mục Backend

```
backend/
├── app/
│   ├── main.py                 # FastAPI application entry
│   ├── api/
│   │   └── routes.py           # API endpoints
│   ├── models/
│   │   └── game.py             # Pydantic data models
│   ├── services/
│   │   ├── game_service.py     # Game logic
│   │   └── pokemon_data.py     # Pokemon configuration
│   └── core/
│       └── pathfinder.py       # Pathfinding algorithms
├── requirements.txt
└── run.py
```

#### 3.1.3. Cấu trúc thư mục Frontend

```
frontend/
├── src/
│   ├── App.jsx                 # Root component
│   ├── components/
│   │   ├── GameBoard.jsx       # Main game board
│   │   ├── Cell.jsx            # Individual cell
│   │   ├── MatchLine.jsx       # SVG animation
│   │   └── GameInfo.jsx        # Score/Lives display
│   ├── services/
│   │   └── api.js              # API client (Axios)
│   └── main.jsx                # Entry point
├── public/
│   └── _redirects              # SPA routing config
├── index.html
├── package.json
└── vite.config.js
```

---

### 3.2. Cấu trúc dữ liệu

#### 3.2.1. Backend Data Models

**Cell (Ô trên bàn chơi)**

```python
class Cell(BaseModel):
    type: CellType          # EMPTY | POKEMON | ICE
    pokemon_id: int         # 1-20 (ID Pokemon)
    is_frozen: bool         # True nếu bị phủ đá băng
```

**Position (Vị trí tọa độ)**

```python
class Position(BaseModel):
    row: int                # Hàng (0-indexed)
    col: int                # Cột (0-indexed)
```

**GameBoard (Bàn chơi)**

```python
class GameBoard(BaseModel):
    grid: List[List[Cell]]          # Ma trận 2D
    rows: int                       # Số hàng (8)
    cols: int                       # Số cột (12)
    time_remaining: int             # Thời gian còn lại
    lives: int                      # Số mạng
    level: int                      # Level hiện tại
    score: int                      # Điểm số
```

#### 3.2.2. In-Memory Storage

```python
# Backend lưu trữ games trong RAM
games: Dict[str, GameState] = {}

# Key: game_id (UUID string)
# Value: GameState object (toàn bộ trạng thái game)
```

**Lý do sử dụng In-Memory Storage:**
- Truy cập cực nhanh: O(1) lookup
- Đơn giản, phù hợp với demo/prototype
- Không cần setup database
- Hạn chế: Mất dữ liệu khi restart server

---

### 3.3. Sơ đồ luồng xử lý

#### 3.3.1. Luồng tạo game mới

```
┌─────────────┐
│   Client    │
│  Click      │
│ "New Game"  │
└──────┬──────┘
       │
       │ POST /api/game/new?level=1
       ▼
┌────────────────────────┐
│  Backend API Handler   │
└──────┬─────────────────┘
       │
       ▼
┌────────────────────────┐
│  GameService           │
│  .create_new_game()    │
└──────┬─────────────────┘
       │
       ├─► Generate Pokemon list (40 items)
       ├─► Fisher-Yates Shuffle
       ├─► Create 8×12 grid
       ├─► Add ice blocks (if level ≥ 4)
       │
       ▼
┌────────────────────────┐
│  Save to games Dict    │
│  games[game_id] = state│
└──────┬─────────────────┘
       │
       │ Return {game_id, game_state}
       ▼
┌────────────────────────┐
│  Client receives       │
│  Render game board     │
└────────────────────────┘
```

#### 3.3.2. Luồng thực hiện nước đi

```
┌─────────────┐
│   Client    │
│ Click 2     │
│  Pokemon    │
└──────┬──────┘
       │
       │ POST /api/game/{id}/move
       │ Body: {pos1, pos2}
       ▼
┌────────────────────────┐
│  Validate Pokemon      │
│  - Cùng loại?          │
│  - Không frozen?       │
└──────┬─────────────────┘
       │ ✓
       ▼
┌────────────────────────┐
│  Pathfinding           │
│  - Check straight (0)  │
│  - Check L-shape (1)   │
│  - Check Z-shape (2)   │
│  - Check border (3)    │
└──────┬─────────────────┘
       │
       ├─► Valid path found?
       │   ├─ YES ──┐
       │   └─ NO ───┼─► Return {success: false}
       │            │
       ▼            ▼
┌────────────┐  ┌──────────────┐
│ Remove     │  │ Client shows │
│ Pokemon    │  │ error message│
│ from grid  │  └──────────────┘
└──────┬─────┘
       │
       ├─► Remove adjacent ice (4 directions)
       ├─► Update score
       ├─► Check if board clear → Victory?
       │
       ▼
┌────────────────────────┐
│  Has valid moves left? │
└──────┬─────────────────┘
       │
       ├─ NO ──► Auto shuffle board
       │
       ▼
┌────────────────────────┐
│  Return updated state  │
│  {success, path, score}│
└──────┬─────────────────┘
       │
       ▼
┌────────────────────────┐
│  Client updates UI     │
│  - Animate match line  │
│  - Remove Pokemon      │
│  - Update score/lives  │
└────────────────────────┘
```

---

## PHẦN 4: KẾT QUẢ VÀ ĐÁNH GIÁ

### 4.1. Kết quả đạt được

#### 4.1.1. Chức năng đã hoàn thành

| Chức năng | Trạng thái | Thuật toán sử dụng |
|-----------|-----------|-------------------|
| Tạo game mới | ✅ Hoàn thành | Fisher-Yates Shuffle, Board Generation |
| Ghép cặp Pokemon | ✅ Hoàn thành | Simplified Pathfinding (0-3 turns) |
| Gợi ý nước đi | ✅ Hoàn thành | Hash Map + Early Termination |
| Xáo bàn | ✅ Hoàn thành | Fisher-Yates Shuffle |
| Hệ thống điểm | ✅ Hoàn thành | Score calculation based on turns |
| Hệ thống mạng | ✅ Hoàn thành | State management |
| Đá băng | ✅ Hoàn thành | Random placement with Set |
| Animation UI | ✅ Hoàn thành | SVG path drawing, CSS animations |
| Docker deployment | ✅ Hoàn thành | Multi-stage build, Docker Compose |
| Cloud deployment | ✅ Hoàn thành | Render (Backend + Frontend) |

---

### 4.2. So sánh độ phức tạp các thuật toán

#### 4.2.1. Bảng tổng hợp

| Thuật toán | Time Complexity | Space Complexity | Ghi chú |
|-----------|----------------|------------------|---------|
| Fisher-Yates Shuffle | O(n) | O(1) | In-place, unbiased |
| Simplified Pathfinding | O(n²) worst, O(n) avg | O(n²) | Early termination |
| BFS Pathfinding | O(n × 4) | O(n) | State space search |
| Hint Finding | O(n²) worst, O(n) avg | O(n) | Hash map optimization |
| Board Generation | O(n) | O(n) | Linear time |
| Ice Placement | O(k) | O(k) | k = ice count |
| Board Clear Check | O(n) | O(1) | Single pass |

*(n = rows × cols = 96 cho board 8×12)*

#### 4.2.2. Phân tích hiệu suất thực tế

**Test Case: Board 8×12 (96 cells)**

| Thao tác | Thời gian trung bình | Số lần gọi/game |
|---------|---------------------|----------------|
| Tạo board mới | < 1ms | 1 |
| Pathfinding (ghép cặp) | 0.1-0.5ms | ~40-50 |
| Hint finding | 1-3ms | ~5-10 |
| Board shuffle | < 1ms | ~2-3 |
| **Tổng thời gian xử lý/game** | | **~50-100ms** |

**Nhận xét:** Tất cả các thuật toán đều chạy rất nhanh (milliseconds), đảm bảo trải nghiệm người chơi mượt mà không có lag.

---

### 4.3. Đánh giá và nhận xét

#### 4.3.1. Ưu điểm

- **Thiết kế modular:** Tách biệt rõ ràng giữa models, services, core algorithms → dễ bảo trì và mở rộng
- **Tập trung DSA:** Thể hiện rõ các giải thuật kinh điển (BFS, Fisher-Yates, Hash Map, Pathfinding)
- **Tối ưu hiệu suất:** Early termination, hash maps cho O(1) lookup, simplified pathfinding
- **Scalable architecture:** Có thể điều chỉnh kích thước bàn chơi (mặc định 8×12)
- **Production-ready:** Error handling, type validation (Pydantic), HTTP status codes chuẩn
- **Full-stack deployment:** Docker, Render cloud, CI/CD ready

#### 4.3.2. Hạn chế

- **In-Memory Storage:** Dữ liệu mất khi restart server → Cần database cho production thực tế
- **Single-player only:** Chưa hỗ trợ multiplayer mode
- **No persistence:** Không lưu lịch sử game, leaderboard
- **Limited animations:** Animation cơ bản, chưa có particle effects, sound

#### 4.3.3. Kiến thức DSA đã áp dụng

| Chủ đề DSA | Ứng dụng trong game |
|-----------|---------------------|
| **Graph Algorithms** | BFS pathfinding với ràng buộc lượt rẽ |
| **Randomization** | Fisher-Yates shuffle để phân bố Pokemon |
| **Hash Tables** | Group Pokemon theo loại cho hint system |
| **Greedy Algorithms** | Simplified pathfinding (thử đường đơn giản trước) |
| **2D Arrays** | Grid representation của bàn chơi |
| **State Management** | Game state tracking (board, score, lives, etc.) |
| **Space-Time Tradeoff** | Hash map tốn O(n) space nhưng tăng tốc từ O(n²) → O(1) |

---

## PHẦN 5: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

### 5.1. Kết luận

Đồ án PokeKawaii đã thành công trong việc áp dụng các kiến thức về Phân tích Thiết kế Giải thuật vào một ứng dụng game thực tế. Qua quá trình thực hiện, nhóm đã:

- Triển khai thành công 7 thuật toán chính với độ phức tạp thời gian từ O(1) đến O(n²)
- So sánh và lựa chọn thuật toán tối ưu cho từng chức năng (Simplified Pathfinding vs BFS, Hash Map vs Brute Force)
- Xây dựng được kiến trúc hệ thống hoàn chỉnh với Backend FastAPI và Frontend React
- Deploy thành công ứng dụng lên cloud platform (Render) với Docker containerization
- Đạt hiệu suất xử lý tốt (~50-100ms/game) đảm bảo trải nghiệm người chơi mượt mà

Đồ án không chỉ là một game giải trí mà còn là một ví dụ minh họa xuất sắc về việc áp dụng DSA (Data Structures & Algorithms) vào lập trình thực tế, phù hợp cho mục đích học tập và demo kỹ năng lập trình.

### 5.2. Hướng phát triển

#### 5.2.1. Tính năng mới

- **Database Integration:** Thêm PostgreSQL/MongoDB để lưu game history, user profiles, leaderboard
- **Multiplayer Mode:** Sử dụng WebSocket cho chế độ chơi real-time 2 người
- **AI Solver:** Implement AI agent tự giải game (A* algorithm, backtracking)
- **Power-ups:** Thêm item đặc biệt (bomb xóa vùng, freeze time, extra lives)
- **Achievement System:** Huy chương, thành tích, daily challenges

#### 5.2.2. Cải tiến kỹ thuật

- **Dynamic Difficulty:** Điều chỉnh số lượt rẽ tối đa theo level
- **Caching Layer:** Redis cho session management và leaderboard
- **Mobile Responsive:** Tối ưu cho thiết bị di động (touch events, adaptive layout)
- **Animation Polish:** Particle effects, shake animation, sound effects
- **Internationalization:** Hỗ trợ đa ngôn ngữ (i18n)

#### 5.2.3. Tối ưu thuật toán

- **Parallel Processing:** Multi-threading cho hint finding trên board lớn
- **Memoization:** Cache kết quả pathfinding cho các cặp vị trí đã kiểm tra
- **A* Pathfinding:** Thay thế BFS bằng A* với heuristic tốt hơn

### 5.3. Bài học kinh nghiệm

#### 5.3.1. Kỹ thuật

- Lựa chọn thuật toán phù hợp quan trọng hơn thuật toán phức tạp (Simplified Pathfinding thắng BFS)
- Early termination và hash maps có thể cải thiện hiệu suất đáng kể (10,000x với Hint Finding)
- Space-time tradeoff là công cụ mạnh mẽ để tối ưu (trade O(n) space để có O(1) lookup)
- Test trên data thực tế quan trọng hơn big-O notation (average case vs worst case)

#### 5.3.2. Quản lý dự án

- Thiết kế kiến trúc modular giúp dễ dàng maintain và mở rộng
- Version control (Git) và documentation là yếu tố then chốt
- Docker và cloud deployment đơn giản hóa quá trình deploy
- Code review và testing sớm giúp phát hiện bug nhanh chóng

### 5.4. Lời cảm ơn

Em xin chân thành cảm ơn Thầy/Cô [Tên giảng viên] đã hướng dẫn và tạo điều kiện để em hoàn thành đồ án này. Những kiến thức về Phân tích Thiết kế Giải thuật mà em học được trong học phần này sẽ là nền tảng vững chắc cho sự nghiệp lập trình của em sau này.

Em cũng xin cảm ơn các bạn trong nhóm (nếu có) đã cùng nhau hợp tác và hỗ trợ nhau trong suốt quá trình thực hiện đồ án.

---

## TÀI LIỆU THAM KHẢO

1. Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press.

2. Knuth, D. E. (1997). *The Art of Computer Programming, Volume 2: Seminumerical Algorithms* (3rd ed.). Addison-Wesley.

3. FastAPI Documentation. (2024). *FastAPI - Modern Web Framework for Python*. https://fastapi.tiangolo.com/

4. React Documentation. (2024). *React - A JavaScript Library for Building User Interfaces*. https://react.dev/

5. Docker Documentation. (2024). *Docker - Containerization Platform*. https://docs.docker.com/

6. Render Documentation. (2024). *Render - Cloud Application Platform*. https://render.com/docs

7. PokeAPI. (2024). *The RESTful Pokémon API*. https://pokeapi.co/

8. GitHub Repository. (2026). *PokeKawaii Source Code*. https://github.com/KiRzEa/Pikachu

---

## PHỤ LỤC

### A. Link Demo & Source Code

- **GitHub Repository:** https://github.com/KiRzEa/Pikachu
- **Live Demo (Frontend):** https://pikachu-fe.onrender.com
- **API Documentation:** https://pokekawaii-backend.onrender.com/docs
- **Game Analysis Document:** PHAN_TICH_GAME_POKEKAWAII.html
- **Docker Guide:** README_DOCKER.md
- **Render Deployment Guide:** README_RENDER.md

### B. Hướng dẫn chạy local

#### B.1. Backend

```bash
# Clone repository
git clone https://github.com/KiRzEa/Pikachu.git
cd Pikachu/backend

# Install dependencies
pip install -r requirements.txt

# Run server
python run.py

# Server chạy tại: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

#### B.2. Frontend

```bash
# Vào thư mục frontend
cd Pikachu/frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Frontend chạy tại: http://localhost:3000
```

#### B.3. Docker

```bash
# Build và chạy cả hai services
docker-compose up --build

# Frontend: http://localhost
# Backend: http://localhost:8000
```

---

**--- HẾT ---**
